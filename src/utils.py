#!/usr/bin/env python3

import time
from functools import wraps


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


def cache(seconds):
    """
    Decorator to cache the result of a function for a specified number of seconds in memory.

    This decorator stores the result of the function call along with the current timestamp.
    If the function is called again with the same arguments within the cache duration,
    the cached result is returned instead of recomputing the result.

    Parameters:
    ----------
    seconds : int or float
        The number of seconds to cache the result for.

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

        @wraps(func)
        def wrapped(*args, **kwargs):
            key = (make_hashable(args), make_hashable(kwargs))
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < seconds:
                    return result

            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result

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
