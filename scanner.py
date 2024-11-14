# scanner.py

from data_fetch import fetch_data
from indicators import calculate_ema, calculate_sma, calculate_wma, calculate_adx, calculate_macd, calculate_rsi, calculate_fibonacci_levels
import pandas as pd
import logging
from tqdm import tqdm

logger = logging.getLogger()

def scan_symbols(symbols, ema_short=20, ema_long=50, wma_short=20, wma_long=50, hma_short=7, hma_long=200, threshold=0.5, volume_threshold=10):
    """Sembolleri tarar ve EMA/WMA/HMA kesişim sonuçlarını toplar."""
    ema_results = []
    wma_results = []
    near_ema_results = []
    near_wma_results = []
    hma_results = []
    
    # tqdm ile ilerleme çubuğu ekleme
    for symbol in tqdm(symbols, desc="Processing Symbols"):
        data = fetch_data(symbol)
        if data is None:
            continue

        # EMA Taraması
        data['EMA_Short'] = calculate_ema(data['close'], ema_short)
        data['EMA_Long'] = calculate_ema(data['close'], ema_long)
        data['BullishCross'] = (data['EMA_Short'] > data['EMA_Long']) & (data['EMA_Short'].shift(1) <= data['EMA_Long'].shift(1))
        ema_last_row = data.iloc[-1]
        
        if ema_last_row['BullishCross']:
            ema_results.append({
                'Symbol': symbol, 
                'Last Price': ema_last_row['close'], 
                'Date': ema_last_row['datetime']
            })

        # WMA Taraması
        data['WMA_Short'] = calculate_wma(data['close'], wma_short)
        data['WMA_Long'] = calculate_wma(data['close'], wma_long)
        data['BullishWmaCross'] = (data['WMA_Short'] > data['WMA_Long']) & (data['WMA_Short'].shift(1) <= data['WMA_Long'].shift(1))
        wma_last_row = data.iloc[-1]
        
        if wma_last_row['BullishWmaCross']:
            wma_results.append({
                'Symbol': symbol, 
                'Last Price': wma_last_row['close'], 
                'Date': wma_last_row['datetime']
            })

        # HMA Kesişimi
        data['HMA_Short'] = calculate_wma(data['close'], hma_short)
        data['HMA_Long'] = calculate_wma(data['close'], hma_long)
        data['BullishHMACross'] = (data['HMA_Short'] > data['HMA_Long']) & (data['HMA_Short'].shift(1) <= data['HMA_Long'].shift(1))
        hma_last_row = data.iloc[-1]
        
        if hma_last_row['BullishHMACross']:
            hma_results.append({
                'Symbol': symbol, 
                'Last Price': hma_last_row['close'], 
                'Date': hma_last_row['datetime'], 
                'Signal': '7 HMA crossed above 200 HMA'
            })

    # Sonuçları döndürme
    return {
        'ema': pd.DataFrame(ema_results),
        'wma': pd.DataFrame(wma_results),
        'near_ema': pd.DataFrame(near_ema_results),
        'near_wma': pd.DataFrame(near_wma_results),
        'hma': pd.DataFrame(hma_results)
    }

# 13/34 EMA Crossover kontrol fonksiyonu
def check_ema_crossover_13_34(data):
    """13/34 EMA Crossover stratejisini kontrol eder."""
    data['EMA13'] = calculate_ema(data['close'], 13)
    data['EMA34'] = calculate_ema(data['close'], 34)
    data['SMA200'] = calculate_sma(data['close'], 200)

    data['Condition'] = (
        (data['EMA13'] > data['EMA34']) &
        (data['EMA13'].shift(1) <= data['EMA34'].shift(1)) &  # Crossover condition
        (data['EMA13'] > data['SMA200'])  # EMA13 is above SMA200
    )
    return data
