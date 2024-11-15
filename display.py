import matplotlib.pyplot as plt
import os
import requests

def plot_results(data, symbol, condition, last_price, volume, date, strategy="Default", show_on_screen=False):
    """Fiyat ve stratejiye uygun göstergeleri içeren bir grafik oluşturur, kaydeder ve isteğe bağlı olarak ekrana gösterir."""
    fig, ax1 = plt.subplots(1, 1, figsize=(12, 6))

    # Fiyat grafiği
    ax1.plot(data['datetime'], data['close'], label="Close Price", color="blue")
    ax1.set_title(f"{symbol} - {condition} ({strategy})")
    ax1.set_ylabel("Price")
    ax1.axhline(last_price, color="green", linestyle="--", label=f"Last Price: {last_price}")
    ax1.legend()

    # Stratejiye bağlı olarak ek göstergeler
    if "EMA" in strategy:
        ax1.plot(data['datetime'], data['EMA_Short'], label="EMA Short", color="orange")
        ax1.plot(data['datetime'], data['EMA_Long'], label="EMA Long", color="purple")
    if "WMA" in strategy:
        ax1.plot(data['datetime'], data['WMA_Short'], label="WMA Short", color="red")
        ax1.plot(data['datetime'], data['WMA_Long'], label="WMA Long", color="brown")
    if "HMA" in strategy:
        ax1.plot(data['datetime'], data['HMA_Short'], label="HMA Short", color="cyan")
        ax1.plot(data['datetime'], data['HMA_Long'], label="HMA Long", color="magenta")

    ax1.legend()

    # Dosyayı kaydet
    file_name = f"{symbol}_{date}_{strategy}.png"
    plt.tight_layout()
    plt.savefig(file_name)

    # Ekrana gösterim
    if show_on_screen:
        plt.show()

    plt.close()
    return file_name

def send_to_telegram(bot_token, chat_id, file_path, caption):
    """Grafiği ve açıklamayı Telegram'a gönderir."""
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(file_path, 'rb') as photo:
        payload = {
            "chat_id": chat_id,
            "caption": caption,
            "parse_mode": "HTML"
        }
        files = {"photo": photo}
        try:
            response = requests.post(url, data=payload, files=files)
            response.raise_for_status()
            print(f"Grafik Telegram'a gönderildi: {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Telegram gönderim hatası: {e}")
