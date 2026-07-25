import pandas as pd
import matplotlib.pyplot as plt

df22 = pd.read_csv("data/district_wise_2022.csv")
df23 = pd.read_csv("data/district_wise_2023.csv")

df22["Year"] = 2022
df23["Year"] = 2023

combined = pd.concat([df22, df23])

district_totals = (
    combined.groupby("Year")["Total"]
    .sum()
)

print(district_totals)

district_totals.plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Total Karnataka Crimes")
plt.ylabel("Cases")
plt.show()