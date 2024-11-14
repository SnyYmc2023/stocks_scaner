# indicators.py

import pandas as pd
import numpy as np

def check_ema_crossover_near(data, short_period, long_period, threshold=0.5):
    """EMA kısa ve uzun periyotları için kesişime yakın kontrol"""
    data['EMA_Short'] = data['close'].ewm(span=short_period, adjust=False).mean()
    data['EMA_Long'] = data['close'].ewm(span=long_period, adjust=False).mean()
    data['BullishCross'] = (data['EMA_Short'] > data['EMA_Long']) & (data['EMA_Short'].shift(1) <= data['EMA_Long'].shift(1))
    data['NearCross'] = (abs(data['EMA_Short'] - data['EMA_Long']) <= threshold)
    return data

def check_wma_crossover_near(data, short_period, long_period, threshold=0.5):
    """WMA kısa ve uzun periyotları için kesişime yakın kontrol"""
    data['WMA_Short'] = calculate_wma(data['close'], short_period)
    data['WMA_Long'] = calculate_wma(data['close'], long_period)
    data['BullishCross'] = (data['WMA_Short'] > data['WMA_Long']) & (data['WMA_Short'].shift(1) <= data['WMA_Long'].shift(1))
    data['NearCross'] = (abs(data['WMA_Short'] - data['WMA_Long']) <= threshold)
    return data

def calculate_hma(series, period):
    """Hull Moving Average (HMA) hesaplama"""
    half_length = int(period / 2)
    sqrt_length = int(np.sqrt(period))
    wma_half = calculate_wma(series, half_length)
    wma_full = calculate_wma(series, period)
    raw_hma = 2 * wma_half - wma_full
    return calculate_wma(raw_hma, sqrt_length)

def calculate_wma(series, period):
    """Weighted Moving Average (WMA) hesaplama"""
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

def calculate_ema(series, period):
    """Exponential Moving Average (EMA) hesaplama"""
    return series.ewm(span=period, adjust=False).mean()

def calculate_sma(series, period):
    """Simple Moving Average (SMA) hesaplama"""
    return series.rolling(window=period).mean()
