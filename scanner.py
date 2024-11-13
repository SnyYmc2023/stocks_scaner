# scanner.py

from data_fetch import fetch_data
from indicators import check_ema_crossover_near, check_wma_crossover_near
import pandas as pd
import logging

logger = logging.getLogger()

def scan_symbols(symbols, ema_short=20, ema_long=50, wma_short=20, wma_long=50, threshold=0.5, volume_threshold=10):
    """Sembolleri tarar ve EMA/WMA kesişim sonuçlarını toplar."""
    ema_results = []
    wma_results = []
    near_ema_results = []
    near_wma_results = []
    
    for symbol in symbols:
        data = fetch_data(symbol)
        if data is None:
            continue

        # EMA Taraması
        ema_data = check_ema_crossover_near(data.copy(), ema_short, ema_long, threshold)
        ema_last_row = ema_data.iloc[-1]
        if ema_last_row['BullishCross']:
            ema_results.append({
                'Symbol': symbol,
                'Last Price': ema_last_row['close'],
                'Date': ema_last_row['datetime']
            })
        elif ema_last_row['NearCross'] and ema_last_row.get('volume', 0) >= volume_threshold:
            near_ema_results.append({
                'Symbol': symbol,
                'Last Price': ema_last_row['close'],
                'Date': ema_last_row['datetime'],
                'Volume': ema_last_row['volume']
            })

        # WMA Taraması
        wma_data = check_wma_crossover_near(data.copy(), wma_short, wma_long, threshold)
        wma_last_row = wma_data.iloc[-1]
        if wma_last_row['BullishCross']:
            wma_results.append({
                'Symbol': symbol,
                'Last Price': wma_last_row['close'],
                'Date': wma_last_row['datetime']
            })
        elif wma_last_row['NearCross'] and wma_last_row.get('volume', 0) >= volume_threshold:
            near_wma_results.append({
                'Symbol': symbol,
                'Last Price': wma_last_row['close'],
                'Date': wma_last_row['datetime'],
                'Volume': wma_last_row['volume']
            })

    # Sonuçları döndürme
    return {
        'ema': pd.DataFrame(ema_results),
        'near_ema': pd.DataFrame(near_ema_results),
        'wma': pd.DataFrame(wma_results),
        'near_wma': pd.DataFrame(near_wma_results)
    }
