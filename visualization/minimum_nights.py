import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("airbnb_data_renamed.csv")

plt.style.use("seaborn")

# plot a histogram of minimum_nights
df.minimum_nights.plot(kind="hist", range=(0, 60), bins=30)

plt.title("Distribution of minimum_nights", fontsize=20)
plt.xlabel("Number of Nights", fontsize=16)
plt.ylabel("Frequency", fontsize=16)

plt.savefig("./figures/minimum_nights.png")