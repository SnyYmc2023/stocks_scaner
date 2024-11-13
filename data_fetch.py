# data_fetch.py

import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import logging

# TvDatafeed başlatma
tv = TvDatafeed()
logger = logging.getLogger()

# Sembol grupları için URL'ler
SYMBOL_GROUP_URLS = {
    "bist30": "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/Bist30.txt",
    "bist50": "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/Bist50.txt",
    "bist100": "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/Bist100.txt",
    "anapazar": "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/anapazar.txt",
    "yildizpazar": "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/yildizpazar.txt"
}

def get_symbols(group="tümü"):
    """Belirtilen grup için sembolleri getirir."""
    if group in SYMBOL_GROUP_URLS:
        url = SYMBOL_GROUP_URLS[group]
        symbols = pd.read_csv(url, header=None)[0].tolist()
        return [f'BIST:{symbol}' for symbol in symbols]
    elif group == "tümü":
        logger.warning("Tüm semboller için liste sağlanamıyor. Lütfen bir grup belirtin.")
        return []
    else:
        logger.warning(f"Geçersiz grup '{group}'. Varsayılan olarak BIST30 kullanılıyor.")
        url = SYMBOL_GROUP_URLS["bist30"]
        symbols = pd.read_csv(url, header=None)[0].tolist()
        return [f'BIST:{symbol}' for symbol in symbols]

def fetch_data(symbol, n_bars=100, interval=Interval.in_daily):
    """Belirtilen sembol için veri çeker."""
    try:
        data = tv.get_hist(symbol=symbol, exchange="BIST", interval=interval, n_bars=n_bars)
        return data.reset_index()
    except Exception as e:
        logger.error(f"Failed to fetch data for {symbol}: {e}")
        return None
