# config.py

class Config:
    # Telegram Ayarları
    BOT_TOKEN = "your_bot_token"  # Telegram bot tokenını buraya ekleyin
    CHAT_ID = "your_chat_id"  # Telegram chat_id'sini buraya ekleyin

    # Tarama Ayarları
    ENABLE_EMA_SCAN = True
    ENABLE_NEAR_EMA_SCAN = True
    ENABLE_WMA_SCAN = True
    ENABLE_NEAR_WMA_SCAN = True
    ENABLE_HMA_SCAN = True
    ENABLE_EMA_13_34_CROSSOVER = True

    # Periyotlar
    EMA_PERIOD_SHORT = 20
    EMA_PERIOD_LONG = 50
    WMA_PERIOD_SHORT = 20
    WMA_PERIOD_LONG = 50
    HMA_PERIOD_SHORT = 7
    HMA_PERIOD_LONG = 200

    # Diğer Parametreler
    NEAR_THRESHOLD = 0.5
    DEFAULT_VOLUME_THRESHOLD = 10
    SYMBOL_GROUP = "bist50"
