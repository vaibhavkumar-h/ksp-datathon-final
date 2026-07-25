import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/district_wise_2024.csv")

# Remove heading row
df = df.dropna(subset=["Sl No"])

crime_columns = [
    "MURDER",
    "RAPE",
    "THEFT",
    "CYBER CRIME",
    "POCSO"
]

totals = df[crime_columns].sum()

print(totals)

plt.figure(figsize=(10,6))

totals.plot(
    kind="bar"
)

plt.title("Major Crime Categories in Karnataka (2024)")
plt.ylabel("Cases")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()