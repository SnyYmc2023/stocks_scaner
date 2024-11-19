import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import logging

logger = logging.getLogger()

# TvDatafeed başlatma (kimlik bilgileri olmadan anonim giriş)
tv = TvDatafeed()

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
    try:
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
    except Exception as e:
        logger.error(f"Sembol grupları alınırken hata oluştu: {e}")
        return []

def fetch_data(symbol, n_bars=100, interval=Interval.in_daily):
    """Belirtilen sembol için veri çeker."""
    try:
        # Interval türünü string'e çevir
        if isinstance(interval, Interval):
            interval = str(interval)

        # Veriyi çek
        data = tv.get_hist(symbol=symbol, exchange="BIST", interval=interval, n_bars=n_bars)
        if data is not None and not data.empty:
            data.reset_index(inplace=True)
            data['datetime'] = pd.to_datetime(data['datetime'])  # Tarih sütununu datetime formatına çevir
            return data
        else:
            logger.warning(f"{symbol} için veri bulunamadı.")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"{symbol} için veri alınırken hata oluştu: {e}")
        return pd.DataFrame()
