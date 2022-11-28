import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("airbnb_data_renamed.csv")

plt.style.use("seaborn")

# plot a histogram of calculated_host_listings_count
df.calculated_host_listings_count.plot(kind="hist", range=(0, 10), bins=10)

plt.title("Distribution of calculated_host_listings_count", fontsize=20)
plt.xlabel("Number of Apartments", fontsize=16)
plt.ylabel("Frequency", fontsize=16)

plt.savefig("./figures/calculated_host_listings_count.png")