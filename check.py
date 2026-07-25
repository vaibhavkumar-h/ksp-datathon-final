import pandas as pd
df = pd.read_csv("data/fir_karnataka.csv")  # adjust filename to whatever it's actually called
print(list(df.columns))
print(df.head())
print(len(df))