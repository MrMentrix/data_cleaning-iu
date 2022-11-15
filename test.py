import pandas as pd

data = pd.read_csv("airbnb_data_cleaned.csv")

x = data["neighbourhood"].unique()
x.sort()
print(x)