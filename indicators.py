# indicators.py

import numpy as np
import pandas as pd

def calculate_ema(data, period):
    """EMA hesaplar."""
    return data.ewm(span=period, adjust=False).mean()

def calculate_wma(data, period):
    """WMA hesaplar."""
    weights = np.arange(1, period + 1)
    return data.rolling(period).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

def calculate_hma(data, period):
    """HMA hesaplar."""
    half_period_wma = calculate_wma(data, period // 2)
    full_period_wma = calculate_wma(data, period)
    hma_data = 2 * half_period_wma - full_period_wma
    return calculate_wma(hma_data, int(np.sqrt(period)))  # Son adımda karekök periyodla WMA
