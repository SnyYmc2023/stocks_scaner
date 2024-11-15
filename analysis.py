import pandas as pd
from data_fetch import fetch_data
from indicators import calculate_ema, calculate_wma, calculate_hma

def get_and_analyze_data(symbol, timeframe):
    """Sembol için verileri alır ve analiz eder."""
    data = fetch_data(symbol, timeframe)
    if data is None or data.empty:
        return pd.DataFrame()  # Eğer veri yoksa boş bir DataFrame döner

    # EMA hesaplamaları
    data['EMA_Short'] = calculate_ema(data['close'], 20)  # Örnek kısa EMA periyodu
    data['EMA_Long'] = calculate_ema(data['close'], 50)   # Örnek uzun EMA periyodu

    # WMA hesaplamaları
    data['WMA_Short'] = calculate_wma(data['close'], 20)
    data['WMA_Long'] = calculate_wma(data['close'], 50)

    # HMA hesaplamaları
    data['HMA_Short'] = calculate_hma(data['close'], 7)
    data['HMA_Long'] = calculate_hma(data['close'], 200)

    return data
