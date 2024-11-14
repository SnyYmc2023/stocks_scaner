from data_fetch import fetch_data
from indicators import calculate_ema, calculate_sma, calculate_wma, calculate_adx, calculate_macd, calculate_rsi, calculate_fibonacci_levels
import pandas as pd
import logging
from tqdm import tqdm

logger = logging.getLogger()

# Moving Average Bullish Strong Buy kontrol fonksiyonu
def check_ma_bullish_conditions(data):
    data['EMA5'] = calculate_ema(data['close'], 5)
    data['SMA20'] = calculate_sma(data['close'], 20)
    data['SMA40'] = calculate_sma(data['close'], 40)
    data['SMA50'] = calculate_sma(data['close'], 50)
    data['WMA10'] = calculate_wma(data['close'], 10)
    data['ADX'], data['ADX_pos'], data['ADX_neg'] = calculate_adx(data, 14)
    data['MACD_line'], data['MACD_signal'] = calculate_macd(data)
    data['RSI'] = calculate_rsi(data, 14)

    data['Condition'] = (
        (data['EMA5'] > data['SMA20']) &
        (data['WMA10'] > data['SMA20']) &
        (data['ADX_pos'] > 20) &
        (data['ADX'] > 20) &
        (data['volume'] > 100000) &
        (data['MACD_line'] > 0) &
        (data['close'] > data['close'].shift(1)) &
        (data['close'] > data['SMA50']) &
        (data['close'] > 150) &
        (data['ADX_pos'] > data['ADX_neg']) &
        (data['RSI'] > 50) &
        (data['MACD_line'] > data['MACD_signal']) &
        (data['close'] > data['close'].shift(2)) &
        (data['SMA20'] > data['SMA40'])
    )
    return data

# 13/34 EMA Crossover kontrol fonksiyonu
def check_ema_crossover_conditions(data):
    data['EMA13'] = calculate_ema(data['close'], 13)
    data['EMA34'] = calculate_ema(data['close'], 34)
    data['SMA200'] = calculate_sma(data['close'], 200)

    data['Condition'] = (
        (data['EMA13'] > data['SMA200']) &
        (data['EMA13'] > data['EMA34']) &
        (data['EMA13'].shift(1) <= data['EMA34'].shift(1)) &
        (data['SMA200'] > data['SMA200'].shift(1)) &
        (data['volume'] >= 1000000)
    )
    return data

# Fibonacci ve Güç Stratejisi kontrol fonksiyonu
def check_fibo_conditions(data):
    data = calculate_fibonacci_levels(data, period=55)

    data['enter_long'] = (
        ((data['close'].iloc[-1] - data['open'].iloc[-1]) / (data['high'].iloc[-1] - data['low'].iloc[-1]) > 0.50) &
        (data['low'].iloc[-1] > (data['min_low'].iloc[-1] + (data['max_high'].iloc[-1] - data['min_low'].iloc[-1]) * 0.382) * 0.99) &
        (data['low'].iloc[-2] <= (data['min_low'].iloc[-2] + (data['max_high'].iloc[-2] - data['min_low'].iloc[-2]) * 0.382) * 0.99) &
        (data['volume'].iloc[-1] > 1000000)
    )

    return data
