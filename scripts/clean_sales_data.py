"""
Basic data cleaning script for sales dataset.
Author: Matthew McDuffie
"""

import pandas as pd

def clean_sales_data(input_path, output_path):
    df = pd.read_csv(input_path)
    df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
    df.dropna(how='all', inplace=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned file saved to: {output_path}")

if __name__ == "__main__":
    clean_sales_data("../data/sales.csv", "../output/cleaned_data/cleaned_sales.csv")
