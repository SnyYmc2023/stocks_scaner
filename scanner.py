# scanner.py

from data_fetch import fetch_data
from indicators import check_ema_crossover_near, check_wma_crossover_near, calculate_hma
import pandas as pd
import logging
from tqdm import tqdm

logger = logging.getLogger()

def scan_symbols(tv, symbols, ema_short=20, ema_long=50, wma_short=20, wma_long=50, hma_short=7, hma_long=200, threshold=0.5, volume_threshold=10):
    """Sembolleri tarar ve EMA/WMA/HMA kesişim sonuçlarını toplar."""
    ema_results = []
    wma_results = []
    near_ema_results = []
    near_wma_results = []
    hma_results = []
    
    # tqdm ile ilerleme çubuğu ekleme
    for symbol in tqdm(symbols, desc="Processing Symbols"):
        data = fetch_data(tv, symbol)  # tv nesnesini burada geçiyoruz
        if data is None:
            continue

        # EMA Taraması
        ema_data = check_ema_crossover_near(data.copy(), ema_short, ema_long, threshold)
        ema_last_row = ema_data.iloc[-1]
        guncel_fiyat = ema_last_row['close']
        hacim = ema_last_row.get('volume', 0)

        if ema_last_row['BullishCross']:
            ema_results.append({'Symbol': symbol, 'Last Price': guncel_fiyat, 'Date': ema_last_row['datetime']})
        elif ema_last_row['NearCross'] and hacim >= volume_threshold:
            near_ema_results.append({'Symbol': symbol, 'Last Price': guncel_fiyat, 'Date': ema_last_row['datetime'], 'Volume': hacim})

        # WMA Taraması
        wma_data = check_wma_crossover_near(data.copy(), wma_short, wma_long, threshold)
        wma_last_row = wma_data.iloc[-1]

        if wma_last_row['BullishCross']:
            wma_results.append({'Symbol': symbol, 'Last Price': wma_last_row['close'], 'Date': wma_last_row['datetime']})
        elif wma_last_row['NearCross'] and hacim >= volume_threshold:
            near_wma_results.append({'Symbol': symbol, 'Last Price': wma_last_row['close'], 'Date': wma_last_row['datetime'], 'Volume': hacim})

        # HMA Kesişimi
        data['HMA_Short'] = calculate_hma(data['close'], hma_short)
        data['HMA_Long'] = calculate_hma(data['close'], hma_long)
        data['BullishHMACross'] = (data['HMA_Short'] > data['HMA_Long']) & (data['HMA_Short'].shift(1) <= data['HMA_Long'].shift(1))
        hma_last_row = data.iloc[-1]

        if hma_last_row['BullishHMACross']:
            hma_results.append({'Symbol': symbol, 'Last Price': hma_last_row['close'], 'Date': hma_last_row['datetime'], 'Signal': '7 HMA crossed above 200 HMA'})

    # Sonuçları döndürme
    return {
        'ema': pd.DataFrame(ema_results),
        'near_ema': pd.DataFrame(near_ema_results),
        'wma': pd.DataFrame(wma_results),
        'near_wma': pd.DataFrame(near_wma_results),
        'hma': pd.DataFrame(hma_results)
    }
