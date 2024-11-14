# scanner.py

from data_fetch import fetch_data
from indicators import check_ema_crossover_near, check_wma_crossover_near, calculate_hma, calculate_ema, calculate_sma
import pandas as pd
import logging
from tqdm import tqdm

logger = logging.getLogger()

def scan_symbols(symbols, ema_short=20, ema_long=50, wma_short=20, wma_long=50, hma_short=7, hma_long=200, threshold=0.5, volume_threshold=10):
    """Sembolleri tarar ve EMA/WMA/HMA kesişim sonuçlarını toplar."""
    
    # Temel verileri yükleme
    TEMEL_DATA_URL = "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/temel.txt"
    temel_data = pd.read_csv(TEMEL_DATA_URL, sep='\\t', engine='python')
    
    ema_results = []
    wma_results = []
    near_ema_results = []
    near_wma_results = []
    hma_results = []
    ema_13_34_results = []
    
    for symbol in tqdm(symbols, desc="Processing Symbols"):
        data = fetch_data(symbol)
        if data is None:
            continue

        # Sembolden "BIST:" kısmını kaldır
        symbol_code = symbol.split(':')[1]
        temel_info = temel_data[temel_data['Sembol'] == symbol_code]

        # Eğer temel veriler mevcutsa hesaplamaları yap
        if not temel_info.empty:
            piyasa_degeri = temel_info['Piyasa Değeri'].values[0]
            defter_degeri = temel_info['Defter Değeri'].values[0]
            toplam_hisse_sayisi = temel_info['Toplam Hisse Sayısı'].values[0]
            net_kar = temel_info['Net Kar (Son 4Ç)'].values[0]
            guncel_fiyat = data['close'].iloc[-1]
            hacim = data['volume'].iloc[-1] if 'volume' in data.columns else 0
            
            # PD/DD ve F/K hesaplamaları
            pd_dd = round(piyasa_degeri / defter_degeri, 2) if defter_degeri != 0 else None
            eps = net_kar / toplam_hisse_sayisi if toplam_hisse_sayisi != 0 else None
            fk = round(guncel_fiyat / eps, 2) if eps is not None else None
        else:
            pd_dd = None
            fk = None

        # EMA Taraması
        ema_data = check_ema_crossover_near(data.copy(), ema_short, ema_long, threshold)
        ema_last_row = ema_data.iloc[-1]

        if ema_last_row['BullishCross']:
            ema_results.append({
                'Symbol': symbol, 
                'Last Price': guncel_fiyat, 
                'Date': ema_last_row['datetime'], 
                'PD/DD': pd_dd, 
                'F/K': fk
            })
        elif ema_last_row['NearCross'] and hacim >= volume_threshold:
            near_ema_results.append({
                'Symbol': symbol, 
                'Last Price': guncel_fiyat, 
                'Date': ema_last_row['datetime'], 
                'PD/DD': pd_dd, 
                'F/K': fk, 
                'Volume': hacim
            })

        # WMA Taraması
        wma_data = check_wma_crossover_near(data.copy(), wma_short, wma_long, threshold)
        wma_last_row = wma_data.iloc[-1]

        if wma_last_row['BullishCross']:
            wma_results.append({
                'Symbol': symbol, 
                'Last Price': wma_last_row['close'], 
                'Date': wma_last_row['datetime'], 
                'PD/DD': pd_dd, 
                'F/K': fk
            })
        elif wma_last_row['NearCross'] and hacim >= volume_threshold:
            near_wma_results.append({
                'Symbol': symbol, 
                'Last Price': wma_last_row['close'], 
                'Date': wma_last_row['datetime'], 
                'PD/DD': pd_dd, 
                'F/K': fk, 
                'Volume': hacim
            })

        # HMA Kesişimi
        data['HMA_Short'] = calculate_hma(data['close'], hma_short)
        data['HMA_Long'] = calculate_hma(data['close'], hma_long)
        data['BullishHMACross'] = (data['HMA_Short'] > data['HMA_Long']) & (data['HMA_Short'].shift(1) <= data['HMA_Long'].shift(1))
        hma_last_row = data.iloc[-1]

        if hma_last_row['BullishHMACross']:
            hma_results.append({
                'Symbol': symbol, 
                'Last Price': hma_last_row['close'], 
                'Date': hma_last_row['datetime'], 
                'PD/DD': pd_dd, 
                'F/K': fk, 
                'Signal': '7 HMA crossed above 200 HMA'
            })

        # 13/34 EMA Crossover Taraması
        ema_13_34_data = check_ema_crossover_13_34(data.copy())
        ema_13_34_last_row = ema_13_34_data.iloc[-1]
        
        if ema_13_34_last_row['Condition']:
            ema_13_34_results.append({
                'Symbol': symbol,
                'Last Price': ema_13_34_last_row['close'],
                'Date': ema_13_34_last_row['datetime'],
                'PD/DD': pd_dd,
                'F/K': fk
            })

    return {
        'ema': pd.DataFrame(ema_results),
        'near_ema': pd.DataFrame(near_ema_results),
        'wma': pd.DataFrame(wma_results),
        'near_wma': pd.DataFrame(near_wma_results),
        'hma': pd.DataFrame(hma_results),
        'ema_13_34': pd.DataFrame(ema_13_34_results)
    }

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
