from tabulate import tabulate
import pandas as pd

def display_results(df, title, max_results=None):
    """Sonuçları tablo formatında terminalde görüntüler ve Telegram için tablo oluşturur."""
    if not df.empty:
        # Volume değerlerini sayısal değere çevirme ve bindelik ayraçla biçimlendirme
        if 'Volume' in df.columns:
            # Sadece sayısal olmayanları kontrol etmek ve sıfır olarak doldurmak için dönüştürme
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(-1)
            df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.0f}" if x != -1 else "N/A")  # Hatalı veriler "N/A" olarak işaretlenir.
        
        # Sadece max_results kadar sonuç göstermek için sıralama
        if max_results:
            df = df.sort_values(by="Volume", ascending=False).head(max_results)
        
        # Başlığı ve tablolama
        print(f"\n=== {title} ===\n")
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
