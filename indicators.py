# indicators.py

import pandas as pd
import numpy as np

# Simple Moving Average (SMA) hesaplama
def calculate_sma(series, period):
    return series.rolling(window=period).mean()

# Exponential Moving Average (EMA) hesaplama
def calculate_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

# Weighted Moving Average (WMA) hesaplama
def calculate_wma(series, period):
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

# Average Directional Index (ADX) hesaplama
def calculate_adx(data, period=14):
    data['UpMove'] = data['high'].diff()
    data['DownMove'] = data['low'].diff()
    data['+DM'] = np.where((data['UpMove'] > data['DownMove']) & (data['UpMove'] > 0), data['UpMove'], 0)
    data['-DM'] = np.where((data['DownMove'] > data['UpMove']) & (data['DownMove'] > 0), -data['DownMove'], 0)
    data['TR'] = np.maximum(data['high'] - data['low'], np.maximum(abs(data['high'] - data['close'].shift()), abs(data['low'] - data['close'].shift())))
    data['ATR'] = data['TR'].rolling(window=period).mean()
    data['+DI'] = 100 * (data['+DM'] / data['ATR']).rolling(window=period).mean()
    data['-DI'] = 100 * (data['-DM'] / data['ATR']).rolling(window=period).mean()
    data['DX'] = (abs(data['+DI'] - data['-DI']) / abs(data['+DI'] + data['-DI'])) * 100
    data['ADX'] = data['DX'].rolling(window=period).mean()
    return data['ADX'], data['+DI'], data['-DI']

# MACD hesaplama
def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    short_ema = calculate_ema(data['close'], short_period)
    long_ema = calculate_ema(data['close'], long_period)
    data['MACD_line'] = short_ema - long_ema
    data['MACD_signal'] = calculate_ema(data['MACD_line'], signal_period)
    return data['MACD_line'], data['MACD_signal']

# RSI hesaplama
def calculate_rsi(data, period=14):
    delta = data['close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Fibonacci seviyeleri hesaplama
def calculate_fibonacci_levels(data, period=55):
    data['min_low'] = data['low'].rolling(window=period).min()
    data['max_high'] = data['high'].rolling(window=period).max()
    return data
