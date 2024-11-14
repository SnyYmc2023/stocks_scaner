# data_fetch.py

import pandas as pd
from tvDatafeed import Interval
import logging

logger = logging.getLogger()

# Sembol grupları için URL'ler
SYMBOL_GROUP_URLS = {
    "bist30": "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/Bist30.txt",
    "bist50": "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/Bist50.txt",
    "bist100": "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/Bist100.txt",
    "anapazar": "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/anapazar.txt",
    "yildizpazar": "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/yildizpazar.txt"
}

def get_symbols(tv, group="tümü"):
    """Belirtilen grup için sembolleri getirir."""
    if group == "tümü":
        all_symbols = tv.get_all_symbols(exchange="turkey")
        return [symbol for symbol in all_symbols if 'BIST:' in symbol]
    elif group in SYMBOL_GROUP_URLS:
        url = SYMBOL_GROUP_URLS[group]
        symbols = pd.read_csv(url, header=None)[0].tolist()
        return [f'BIST:{symbol}' for symbol in symbols]
    else:
        logger.warning(f"Geçersiz grup '{group}'. Varsayılan olarak tüm semboller kullanılacak.")
        return get_symbols(tv, "tümü")

def fetch_data(tv, symbol, n_bars=100, interval=Interval.in_daily):
    """Belirtilen sembol için veri çeker."""
    try:
        data = tv.get_hist(symbol=symbol, exchange="BIST", interval=interval, n_bars=n_bars)
        return data.reset_index()
    except Exception as e:
        logger.error(f"Failed to fetch data for {symbol}: {e}")
        return None
