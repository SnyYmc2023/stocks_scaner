# indicators.py

import pandas as pd

def check_ema_crossover_near(data, short_period, long_period, threshold=0.5):
    """EMA kısa ve uzun periyotları için kesişime yakın kontrol"""
    data['EMA_Short'] = data['close'].ewm(span=short_period, adjust=False).mean()
    data['EMA_Long'] = data['close'].ewm(span=long_period, adjust=False).mean()
    data['BullishCross'] = (data['EMA_Short'] > data['EMA_Long']) & (data['EMA_Short'].shift(1) <= data['EMA_Long'].shift(1))
    data['NearCross'] = (abs(data['EMA_Short'] - data['EMA_Long']) <= threshold)
    return data

def check_wma_crossover_near(data, short_period, long_period, threshold=0.5):
    """WMA kısa ve uzun periyotları için kesişime yakın kontrol"""
    data['WMA_Short'] = data['close'].rolling(window=short_period).apply(lambda x: (pd.Series(x).cumsum() * pd.Series(range(1, short_period + 1)).sum()) / short_period)
    data['WMA_Long'] = data['close'].rolling(window=long_period).apply(lambda x: (pd.Series(x).cumsum() * pd.Series(range(1, long_period + 1)).sum()) / long_period)
    data['BullishCross'] = (data['WMA_Short'] > data['WMA_Long']) & (data['WMA_Short'].shift(1) <= data['WMA_Long'].shift(1))
    data['NearCross'] = (abs(data['WMA_Short'] - data['WMA_Long']) <= threshold)
    return data

def calculate_hma(data, period):
    """Hull Moving Average (HMA) hesaplama"""
    return data.rolling(window=period).apply(lambda x: (2 * x.rolling(window=period // 2).mean() - x.rolling(window=period).mean()).mean())

def calculate_ema(data, period):
    """Exponential Moving Average (EMA) hesaplama"""
    return data.ewm(span=period, adjust=False).mean()

def calculate_sma(data, period):
    """Simple Moving Average (SMA) hesaplama"""
    return data.rolling(window=period).mean()
