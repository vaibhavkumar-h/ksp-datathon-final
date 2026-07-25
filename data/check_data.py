import pandas as pd
import os

files = [
    "data/district_wise_2022.csv",
    "data/district_wise_2023.csv",
    "data/district_wise_2024.csv",
    "data/district_wise_2025.csv"
]

for file in files:
    print("\n" + "="*60)
    print(file)

    df = pd.read_csv(file)

    print(df.columns)
    print(df.head())