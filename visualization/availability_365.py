import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("airbnb_data_renamed.csv")

plt.style.use("seaborn")

# plot a histogram of availability_365
df.availability_365.plot(kind="hist", range=(0, 500), bins=50)

print(df["availability_365"].max())
print(df["availability_365"].min())

plt.title("Distribution of availability_365", fontsize=20)
plt.xlabel("Availability Value", fontsize=16)
plt.ylabel("Frequency", fontsize=16)

plt.savefig("./figures/availability_365.png")