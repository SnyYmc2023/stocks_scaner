from tabulate import tabulate
import pandas as pd

def display_results(df, title, max_results=None):
    """Sonuçları tablo formatında terminalde görüntüler ve Telegram için tablo oluşturur."""
    if not df.empty:
        # Volume sütununu kontrol etmek için mevcut verileri yazdırma
        if 'Volume' in df.columns:
            print("Volume sütunundaki veriler:", df['Volume'].head())  # Kontrol amaçlı
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(-1)
            df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.0f}" if x != -1 else "N/A")
        
        # Sadece max_results kadar sonuç göstermek için sıralama
        if max_results:
            df = df.sort_values(by="Volume", ascending=False).head(max_results)
        
        # Başlığı ve tablolama
        print(f"\n=== {title} ===\n")
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
