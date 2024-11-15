from data_fetch import fetch_data
from indicators import (
    check_ema_crossover_near,
    check_wma_crossover_near,
    calculate_hma
)
import pandas as pd
import logging
from tqdm import tqdm

logger = logging.getLogger()

def scan_symbols(symbols, ema_short=None, ema_long=None, wma_short=None, wma_long=None, hma_short=None, hma_long=None, threshold=0.5, volume_threshold=10):
    """Sembolleri tarar ve EMA/WMA/HMA kesişim sonuçlarını toplar."""
    
    # Temel verileri yükleme
    TEMEL_DATA_URL = "https://raw.githubusercontent.com/SinanYMC/bist_analiz/refs/heads/main/temel.txt"
    temel_data = pd.read_csv(TEMEL_DATA_URL, sep='\\t', engine='python')

    # Sonuç listeleri
    ema_results = []
    wma_results = []
    hma_results = []
    near_ema_results = []
    near_wma_results = []
    ema_13_34_results = []

    # tqdm ile ilerleme çubuğu
    for symbol in tqdm(symbols, desc="Processing Symbols"):
        try:
            data = fetch_data(symbol)
            if data is None or data.empty:
                logger.warning(f"No data for symbol: {symbol}")
                continue

            # Temel verilerden sembol bilgisi al
            symbol_code = symbol.split(":")[1]
            temel_info = temel_data[temel_data['Sembol'] == symbol_code]
            if not temel_info.empty:
                piyasa_degeri = temel_info['Piyasa Değeri'].values[0]
                defter_degeri = temel_info['Defter Değeri'].values[0]
                toplam_hisse_sayisi = temel_info['Toplam Hisse Sayısı'].values[0]
                net_kar = temel_info['Net Kar (Son 4Ç)'].values[0]
                guncel_fiyat = data['close'].iloc[-1]
                
                # PD/DD ve F/K hesaplamaları
                pd_dd = round(piyasa_degeri / defter_degeri, 2) if defter_degeri != 0 else None
                eps = net_kar / toplam_hisse_sayisi if toplam_hisse_sayisi != 0 else None
                fk = round(guncel_fiyat / eps, 2) if eps is not None else None
            else:
                pd_dd, fk = None, None

            # EMA Taraması
            if ema_short and ema_long:
                ema_data = check_ema_crossover_near(data.copy(), ema_short, ema_long, threshold)
                ema_last_row = ema_data.iloc[-1]
                if ema_last_row['BullishCross']:
                    ema_results.append({
                        'Symbol': symbol,
                        'Last Price': ema_last_row['close'],
                        'Date': ema_last_row['datetime'],
                        'Volume': ema_last_row.get('volume', 0),
                        'PD/DD': pd_dd,
                        'F/K': fk
                    })
                elif ema_last_row['NearCross'] and ema_last_row.get('volume', 0) >= volume_threshold:
                    near_ema_results.append({
                        'Symbol': symbol,
                        'Last Price': ema_last_row['close'],
                        'Date': ema_last_row['datetime'],
                        'Volume': ema_last_row.get('volume', 0),
                        'PD/DD': pd_dd,
                        'F/K': fk
                    })

            # WMA Taraması
            if wma_short and wma_long:
                wma_data = check_wma_crossover_near(data.copy(), wma_short, wma_long, threshold)
                wma_last_row = wma_data.iloc[-1]
                if wma_last_row['BullishCross']:
                    wma_results.append({
                        'Symbol': symbol,
                        'Last Price': wma_last_row['close'],
                        'Date': wma_last_row['datetime'],
                        'Volume': wma_last_row.get('volume', 0),
                        'PD/DD': pd_dd,
                        'F/K': fk
                    })
                elif wma_last_row['NearCross'] and wma_last_row.get('volume', 0) >= volume_threshold:
                    near_wma_results.append({
                        'Symbol': symbol,
                        'Last Price': wma_last_row['close'],
                        'Date': wma_last_row['datetime'],
                        'Volume': wma_last_row.get('volume', 0),
                        'PD/DD': pd_dd,
                        'F/K': fk
                    })

            # HMA Taraması
            if hma_short and hma_long:
                data['HMA_Short'] = calculate_hma(data['close'], hma_short)
                data['HMA_Long'] = calculate_hma(data['close'], hma_long)
                data['BullishHMACross'] = (data['HMA_Short'] > data['HMA_Long']) & (data['HMA_Short'].shift(1) <= data['HMA_Long'].shift(1))
                hma_last_row = data.iloc[-1]
                if hma_last_row['BullishHMACross']:
                    hma_results.append({
                        'Symbol': symbol,
                        'Last Price': hma_last_row['close'],
                        'Date': hma_last_row['datetime'],
                        'Volume': hma_last_row.get('volume', 0),
                        'Signal': '7 HMA crossed above 200 HMA',
                        'PD/DD': pd_dd,
                        'F/K': fk
                    })

            # 13/34 EMA Taraması
            ema_13_34_data = check_ema_crossover_near(data.copy(), 13, 34, threshold)
            ema_13_34_last_row = ema_13_34_data.iloc[-1]
            if ema_13_34_last_row['BullishCross']:
                ema_13_34_results.append({
                    'Symbol': symbol,
                    'Last Price': ema_13_34_last_row['close'],
                    'Date': ema_13_34_last_row['datetime'],
                    'Volume': ema_13_34_last_row.get('volume', 0),
                    'PD/DD': pd_dd,
                    'F/K': fk
                })

        except Exception as e:
            logger.error(f"Error processing {symbol}: {e}")

    # Sonuçları döndürme
    return {
        'ema': pd.DataFrame(ema_results),
        'near_ema': pd.DataFrame(near_ema_results),
        'wma': pd.DataFrame(wma_results),
        'near_wma': pd.DataFrame(near_wma_results),
        'hma': pd.DataFrame(hma_results),
        'ema_13_34': pd.DataFrame(ema_13_34_results)
    }
