import pandas as pd

print("Reading original dataset...")
df = pd.read_csv("data/fir_karnataka.csv", low_memory=False)

print("Original rows:", len(df))

# Take a random sample of 100,000 rows
sample = df.sample(n=min(100000, len(df)), random_state=42)

print("Sample rows:", len(sample))

sample.to_csv("data/fir_karnataka_small.csv", index=False)

print("Done! Saved as data/fir_karnataka_small.csv")