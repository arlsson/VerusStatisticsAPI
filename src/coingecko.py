#!/usr/bin/env python3

coingecko_ticker_mapping = {}

coingecko_ticker_mapping["VRSC"] = {
      "VRSC_MKR":    "MKR_VRSC"
    , "VRSC_USDT":   "USDT_VRSC"
    , "VRSC_EURC":   "EURC_VRSC"
    , "VRSC_USDC":   "USDC_VRSC"
    , "VRSC_Kaiju":  "Kaiju_VRSC"
    , "VRSC_Switch": "Switch_VRSC"
    , "tBTC_VRSC":   "TBTC_VRSC"
    , "VRSC_whales": "whales_VRSC"
    , "NATI_VRSC":   "NATI.Basket_VRSC"
    , "VRSC_Pure":   "Pure_VRSC"
}

coingecko_ticker_mapping["DAI"] = {
      "DAI_MKR":    "MKR_DAI"
    , "DAI_USDT":   "USDT_DAI"
    , "DAI_EURC":   "EURC_DAI"
    , "DAI_ETH":    "ETH_DAI"
    , "DAI_USDC":   "USDC_DAI"
    , "DAI_Kaiju":  "Kaiju_DAI"
    , "DAI_Switch": "Switch_DAI"
    , "tBTC_DAI":   "TBTC_DAI"
    , "DAI_whales": "whales_DAI"
    , "NATI_DAI":   "NATI.Basket_DAI"
    , "DAI_Pure":   "Pure_DAI"
    , "DAI_VRSC":   "VRSC_DAI"
}

coingecko_ticker_mapping["ETH"] = {
      "ETH_MKR":    "MKR_ETH"
    , "ETH_USDT":   "USDT_ETH"
    , "ETH_EURC":   "EURC_ETH"
    , "ETH_USDC":   "USDC_ETH"
    , "ETH_Kaiju":  "Kaiju_ETH"
    , "ETH_Switch": "Switch_ETH"
    , "tBTC_ETH":   "TBTC_ETH"
    , "ETH_whales": "whales_ETH"
    , "NATI_ETH":   "NATI.Basket_ETH"
    , "ETH_Pure":   "Pure_ETH"
    , "ETH_VRSC":   "VRSC_ETH"
}

coingecko_ticker_mapping["MKR"] = {  
      "MKR_EURC":   "EURC_MKR"
    , "MKR_ETH":    "ETH_MKR"
    , "MKR_USDC":   "USDC_MKR"
    , "MKR_Kaiju":  "Kaiju_MKR"
    , "MKR_Switch": "Switch_MKR"
    , "tBTC_MKR":   "TBTC_MKR"
    , "MKR_whales": "whales_MKR"
    , "NATI_MKR":   "NATI.Basket_MKR"
    , "MKR_Pure":   "Pure_MKR"
    , "MKR_VRSC":   "VRSC_MKR"
}

coingecko_ticker_mapping["BTC"] = {  
      "TBTC_EURC":   "EURC_TBTC"
    , "TBTC_ETH":    "ETH_TBTC"
    , "TBTC_USDC":   "USDC_TBTC"
    , "TBTC_Kaiju":  "Kaiju_TBTC"
    , "TBTC_Switch": "Switch_TBTC"
    , "TBTC_MKR":    "MKR_TBTC"
    , "TBTC_whales": "whales_TBTC"
    , "NATI_TBTC":   "NATI.Basket_TBTC"
    , "TBTC_Pure":   "Pure_TBTC"
    , "TBTC_VRSC":   "VRSC_TBTC"
}