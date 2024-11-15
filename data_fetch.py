# data_fetch.py

import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import logging

logger = logging.getLogger()

# TvDatafeed başlatma (kimlik bilgileri olmadan anonim giriş)
tv = TvDatafeed()
tv.token="eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjo4ODk2ODQsImV4cCI6MTczMTA2OTIwMCwiaWF0IjoxNzMxMDU0ODAwLCJwbGFuIjoicHJvIiwiZXh0X2hvdXJzIjoxLCJwZXJtIjoiYmlzdCIsInN0dWR5X3Blcm0iOiJ0di12b2x1bWVieXByaWNlLHR2LWNoYXJ0cGF0dGVybnMsUFVCOzZlMWMxNGM1ZmU5MjQ2ZWJiODE2MTJhMmRiNzZlNmQ1LFBVQjs1ODZlZWM1ZDExNzc0MGQ0OTUyZWFjZjVjNGUwY2Q2OCIsIm1heF9zdHVkaWVzIjo1LCJtYXhfZnVuZGFtZW50YWxzIjo0LCJtYXhfY2hhcnRzIjoyLCJtYXhfYWN0aXZlX2FsZXJ0cyI6MjAsIm1heF9zdHVkeV9vbl9zdHVkeSI6MSwiZmllbGRzX3Blcm1pc3Npb25zIjpbInJlZmJvbmRzIl0sIm1heF9vdmVyYWxsX2FsZXJ0cyI6MjAwMCwibWF4X2FjdGl2ZV9wcmltaXRpdmVfYWxlcnRzIjoyMCwibWF4X2FjdGl2ZV9jb21wbGV4X2FsZXJ0cyI6MjAsIm1heF9jb25uZWN0aW9ucyI6MTB9.hGJRaGXtEsLsJZLyatPS3nIrnjWxQquLPHTnJgJp7HknSZASy_x5PxpWQVDK2kH2QA_yTRFFXlKIAgHGmlfYMdqD0-dc2-sdlLTAVf0clznsWz1-uuwx3wD_jbxthAgD0cKPm69DVIzndsQVaMn0pEKRYcWKRUv065DQk9x9D90"

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
    if group == "tümü":
        all_symbols = tv.get_all_symbols(exchange="turkey")
        return [symbol for symbol in all_symbols if 'BIST:' in symbol]
    elif group in SYMBOL_GROUP_URLS:
        url = SYMBOL_GROUP_URLS[group]
        symbols = pd.read_csv(url, header=None)[0].tolist()
        return [f'BIST:{symbol}' for symbol in symbols]
    else:
        logger.warning(f"Geçersiz grup '{group}'. Varsayılan olarak tüm semboller kullanılacak.")
        return get_symbols("tümü")

def fetch_data(symbol, n_bars=100, interval=Interval.in_daily):
    """Belirtilen sembol için veri çeker."""
    try:
        data = tv.get_hist(symbol=symbol, exchange="BIST", interval=interval, n_bars=n_bars)
        return data.reset_index()
    except Exception as e:
        logger.error(f"Failed to fetch data for {symbol}: {e}")
        return None
