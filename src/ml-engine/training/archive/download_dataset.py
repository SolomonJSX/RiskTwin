"""
Dataset Downloader for RiskTwin ML Engine.
Downloads recognized open-source credit scoring benchmark datasets:
1. Credit Risk Dataset (Kaggle Benchmark: 32,581 real borrower applications & defaults)
"""

import os
import urllib.request
import pandas as pd

SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
FILE_PATH = os.path.join(SAVE_DIR, "real_credit_risk_dataset.csv")
URL = "https://raw.githubusercontent.com/PhilChodrow/ml-notes/main/data/credit-risk/credit_risk_dataset.csv"

def download_and_inspect():
    print(f"[*] Downloading real benchmark credit risk dataset from: {URL}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req) as response, open(FILE_PATH, 'wb') as out_file:
        data = response.read()
        out_file.write(data)
    
    file_size_kb = os.path.getsize(FILE_PATH) / 1024
    print(f"[+] Download complete: {FILE_PATH} ({file_size_kb:.1f} KB)")

    # Read and inspect
    df = pd.read_csv(FILE_PATH)
    print("\n--- DATASET OVERVIEW ---")
    print(f"Total Rows (Borrowers): {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")
    print("\nTarget (loan_status) Distribution:")
    print(df['loan_status'].value_counts(normalize=True).rename({0: 'Non-Default (0)', 1: 'Default (1)'}))
    print("\nSample Preview (First 3 rows):")
    print(df.head(3))

if __name__ == "__main__":
    download_and_inspect()
