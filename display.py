# display.py

import pandas as pd
from tabulate import tabulate

def display_results(results, title, max_results=None):
    """Sonuçları tablo formatında gösterir."""
    df = pd.DataFrame(results)
    if not df.empty:
        if 'Volume' in df.columns:
            df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.0f}")  # Bindelik ayraç ile gösterim
        if max_results:
            df = df.sort_values(by="Volume", ascending=False).head(max_results)
        print(f"\n{title}\n")
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
