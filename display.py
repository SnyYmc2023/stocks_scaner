from tabulate import tabulate
import pandas as pd

def process_and_send_results(result_df, title):
    if not result_df.empty:
        # Volume değerlerini sayıya çevir ve bindelik ayraçla biçimlendir
        if 'Volume' in result_df.columns:
            result_df['Volume'] = pd.to_numeric(result_df['Volume'], errors='coerce').fillna(0).astype(float)
            result_df['Volume'] = result_df['Volume'].apply(lambda x: f"{x:,.0f}")
        
        # Tablo formatında çıktıyı konsola yazdırma
        display_results(result_df, title)
        
        # Telegram için mesajı tablo formatında oluşturma
        headers = result_df.columns.to_list()
        table_str = tabulate(result_df, headers=headers, tablefmt="grid", showindex=False)
        
        # Telegram mesajı başlığı ile birleştirme
        message = f"=== {title} ===\n\n<pre>{table_str}</pre>"
        
        # Mesajı Telegram'a gönderme
        send_telegram_message(message)
