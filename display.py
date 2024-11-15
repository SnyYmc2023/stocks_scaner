from tabulate import tabulate
import pandas as pd
import requests

def send_telegram_message(message, bot_token, chat_id):
    """Telegram mesajı göndermek için bir işlev."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Message sent to Telegram.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to Telegram: {e}")

def display_results(df, title, max_results=None):
    """Sonuçları terminalde gösterir."""
    if not df.empty:
        if 'Volume' in df.columns:
            # Bindelik ayraç formatında göstermek için Volume sütununu düzenle
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0).astype(int)
            df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.0f}")
        
        if max_results:
            df = df.sort_values(by="Volume", ascending=False).head(max_results)

        print(f"\n=== {title} ===\n")
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

def process_and_send_results(result_df, title, config):
    """Sonuçları terminalde gösterir ve Telegram'a gönderir."""
    if not result_df.empty:
        display_results(result_df, title)
        
        headers = result_df.columns.to_list()
        table_str = tabulate(result_df, headers=headers, tablefmt="grid", showindex=False)
        
        # Telegram mesajı formatı
        message = f"=== {title} ===\n\n<pre>{table_str}</pre>"
        send_telegram_message(message, config.BOT_TOKEN, config.CHAT_ID)
