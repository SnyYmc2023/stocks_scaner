# indicators.py

import numpy as np

def calculate_ema(data, period):
    """EMA hesaplar."""
    return data.ewm(span=period, adjust=False).mean()

def calculate_wma(data, period):
    """WMA hesaplar."""
    weights = np.arange(1, period + 1)
    return data.rolling(period).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

def check_ema_crossover_near(data, short_period, long_period, threshold):
    """EMA kesişimi ve kesişime yakınlık belirler."""
    data['EMA_Short'] = calculate_ema(data['close'], short_period)
    data['EMA_Long'] = calculate_ema(data['close'], long_period)
    data['BullishCross'] = (data['EMA_Short'] > data['EMA_Long']) & (data['EMA_Short'].shift(1) <= data['EMA_Long'].shift(1))
    data['NearCross'] = (data['BullishCross'] == False) & (abs(data['EMA_Short'] - data['EMA_Long']) <= threshold)
    return data

def check_wma_crossover_near(data, short_period, long_period, threshold):
    """WMA kesişimi ve kesişime yakınlık belirler."""
    data['WMA_Short'] = calculate_wma(data['close'], short_period)
    data['WMA_Long'] = calculate_wma(data['close'], long_period)
    data['BullishCross'] = (data['WMA_Short'] > data['WMA_Long']) & (data['WMA_Short'].shift(1) <= data['WMA_Long'].shift(1))
    data['NearCross'] = (data['BullishCross'] == False) & (abs(data['WMA_Short'] - data['WMA_Long']) <= threshold)
    return data
