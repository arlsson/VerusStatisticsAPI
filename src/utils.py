#!/usr/bin/env python3

import os
import time
import pickle
import logging
import hashlib
import threading

from functools import wraps
from collections import defaultdict

logger = logging.getLogger(__name__)


MEMCACHE_HOST = os.getenv("MEMCACHE_HOST", "127.0.0.1")
MEMCACHE_PORT = os.getenv("MEMCACHE_PORT", 11211)

_default_memcached = None
try:
    from pymemcache.client.hash import HashClient
    _default_memcached = HashClient(
        [ ( MEMCACHE_HOST, int(MEMCACHE_PORT) ) ],
        use_pooling = True,
        connect_timeout = 0.1,
        timeout = 0.1,
        no_delay = True,
    )
    _default_memcached.set('test_connection', b'test')
    _default_memcached.get('test_connection')
    logger.info(f"memcache is enabled, {MEMCACHE_HOST}:{MEMCACHE_PORT}")
except Exception:
    logger.error(f"memcache is disabled, {MEMCACHE_HOST}:{MEMCACHE_PORT}")
    _default_memcached = None



def cache(seconds, max_stale = None, memcached_client = None):
    """
    Decorator to cache the result of a function for a specified number of seconds in memory.

    This decorator stores the result of the function call along with the current timestamp.
    If the function is called again with the same arguments within the cache duration,
    the cached result is returned instead of recomputing the result.

    Parameters:
    ----------
    seconds : int or float
        The number of seconds to cache the result for.
    
    max_stale: int or float
        Max time to serve stale data (or None for unlimited)

    memcached_client: 
        Optional external pymemcache client

    Returns:
    -------
    function
        A wrapped function with caching applied.

    Example:
    -------
    @cache(60)
    def compute(a, b):
        return a + b

    # The result of compute(1, 2) will be cached for 60 seconds.
    """
    def decorator(func):
        cache = {}
        timestamps = {}
        update_locks = defaultdict(threading.Lock)

        client = memcached_client or _default_memcached

        @wraps(func)
        def wrapped(*args, **kwargs):
            key = cache_key(func, args, kwargs)

            now = time.time()
            
            if key in cache:
                age = now - timestamps[key]
                
                if age < seconds:
                    return cache[key]  
                
                if max_stale is None or age < max_stale:
                    if not update_locks[key].locked():
                        threading.Thread(target = refresh, args = (func, args, kwargs, key), daemon = True).start()
                    
                    # while refreshing, return cache
                    return cache[key]  

                # wait for results if age is older than max_stale
                result = func(*args, **kwargs)
                store(key, result)
                return result


            if client:
                raw = client.get(key)
                if raw:
                    value, ts = pickle.loads(raw)
                    age = now - ts
                    cache[key] = value
                    timestamps[key] = ts

                    if age < seconds:
                        return value

                    if max_stale is None or age < max_stale:
                        
                        if not update_locks[key].locked():
                            threading.Thread(target = refresh, args=(func, args, kwargs, key), daemon = True).start()
                        
                        return value
                try:
                    pass

                except Exception as e:
                    logger.error(f"cache, wrapped error: {e}")

            # wait for results if no cache is available
            print(f"{func.__module__}.{func.__qualname__} not in cache")
            result = func(*args, **kwargs)
            store(key, result)
            return result


        def refresh(func, args, kwargs, key):
            with update_locks[key]:
                try:
                    result = func(*args, **kwargs)
                    store(key, result)
                    
                except Exception as e:
                    logger.error(f"cache, refresh error: {e}")


        def store(key, result):

            now             = time.time()
            cache[key]      = result
            timestamps[key] = now

            if not client:
                return
            print("memcache update here")
            try:
                client.set(key, pickle.dumps((result, now)), expire=int(max_stale or 60*60*24))
            except Exception as e:
                logger.error(f"cache, store error: {e}")


        def make_hashable(obj):
            """
            Recursively convert unhashable types to hashable ones.
            """

            if isinstance(obj, (tuple, list)):
                return tuple(make_hashable(e) for e in obj)
            
            if isinstance(obj, dict):
                return tuple(sorted((make_hashable(k), make_hashable(v)) for k, v in obj.items()))
            
            if isinstance(obj, set):
                return frozenset(make_hashable(e) for e in obj)
            
            return obj  # Assume obj is already hashable (int, str, etc.)


        def cache_key(func, args, kwargs):
            res = hashlib.md5(f"{func.__module__}.{func.__qualname__}:{make_hashable(args)}:{make_hashable(kwargs)}".encode("utf-8")).hexdigest()
            return res


        return wrapped
    return decorator


def rename_tickers(final_ticker_info, rename_map):
    """
    Rename ticker_ids in final_ticker_info based on a rename_map dictionary.

    Parameters:
    - final_ticker_info: list of dicts, each must have 'ticker_id'
    - rename_map: dict mapping old_id -> new_id

    Returns:
    - None (modifies the list in place)
    """
    for ticker in final_ticker_info:
        old_id = ticker.get('ticker_id')
        if old_id in rename_map:
            ticker['ticker_id'] = rename_map[old_id]
