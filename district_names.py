# district_names.py

import pandas as pd

df = pd.read_csv("data/district_wise_2023.csv")

df = df[df["Districts"] != "TOTAL"]

print(df["Districts"].tolist())