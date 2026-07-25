import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/district_wise_2023.csv")

# Remove TOTAL row
df = df[df["Districts"] != "TOTAL"]

top10 = df.sort_values(
    by="Total",
    ascending=False
).head(10)

print(top10[["Districts", "Total"]])

plt.figure(figsize=(12,6))

plt.bar(
    top10["Districts"],
    top10["Total"]
)

plt.xticks(rotation=45)
plt.ylabel("Crime Cases")
plt.title("Top 10 Crime Districts in Karnataka (2023)")

plt.tight_layout()
plt.show()