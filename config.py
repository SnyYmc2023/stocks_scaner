from tvDatafeed import Interval

class Config:
    # EMA ve WMA periyotları
    EMA_PERIOD_SHORT = 20
    EMA_PERIOD_LONG = 50
    WMA_PERIOD_SHORT = 20
    WMA_PERIOD_LONG = 50
    HMA_PERIOD_SHORT = 7
    HMA_PERIOD_LONG = 200

    # Yakınlık eşiği ve hacim filtresi
    NEAR_THRESHOLD = 0.5
    DEFAULT_VOLUME_THRESHOLD = 10

    # Sembol grubu (örneğin, "bist30", "bist50", "bist100")
    SYMBOL_GROUP = "bist50"

    # Zaman dilimi
    MAIN_TIMEFRAME = "in_daily"  # Günlük veriler
    MTF_TIMEFRAME = "in_4_hour"  # 4 saatlik veriler

    # Telegram bilgileri
    BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    CHAT_ID = "YOUR_CHAT_ID"

    # Tarama seçenekleri
    ENABLE_EMA_SCAN = True
    ENABLE_NEAR_EMA_SCAN = True
    ENABLE_WMA_SCAN = True
    ENABLE_NEAR_WMA_SCAN = True
    ENABLE_HMA_SCAN = True
