import pandas as pd
import matplotlib.pyplot as plt

# reading the (original) data
df = pd.read_csv("airbnb_data.csv")

# REFERENCE: "2.2 Exploring the data"
# renaming all columns into one snake_case format
df.columns = df.columns.str.lower().str.replace(" ", "_")
# saves a renamed version of the original data so working with it is a bit easier
# df.to_csv("airbnb_data_renamed.csv", index=False)

# REFERENCE: "2.2.2 Impossible value ranges" | visualization/minimum_nights.py for visualization code | figures/minimum_nights.png for figure
# putting all values of minimum_nights into the range of 1-30
df["minimum_nights"] = df["minimum_nights"].apply(lambda x: 1 if x < 1 else 30 if x > 30 else x)

# REFERENCE: "2.2.3 Mixed data types"
# converting all values of price and service_fee to floats
df["price"] = df["price"].str.replace("$", "").str.replace(",", "").astype(float)
df["service_fee"] = df["service_fee"].str.replace("$", "").str.replace(",", "").astype(float)

"""HERE"""

for col in df.columns:
    types = []
    for i in df[col]:
        if type(i) not in types:
            types.append(type(i))
    print(col, types)

exit()

# removing all duplicate rows, based on apartment ID
df.drop_duplicates(subset=["id"], inplace=True)

# dropping all rows with missing values
df = df.dropna()

# set all construction years and review rate numbers to be integers
df["construction_year"] = df["construction_year"].astype(int)
df["review_rate_number"] = df["review_rate_number"].astype(int)

# correcting the neighbourhood names
df["neighbourhood_group"] = df["neighbourhood_group"].str.replace("brookln", "Brooklyn")
df["neighbourhood"] = df["neighbourhood"].str.replace("Bay Terrance", "Bay Terrace")

# ensuring that every single neighbourhood only refers to one neighbourhood group
for nh in df["neighbourhood"].unique():
    if len(df[df["neighbourhood"] == nh]["neighbourhood_group"].unique()) > 1:
        most_fequent_group = df[df["neighbourhood"] == nh]["neighbourhood_group"].value_counts().index[0]
        df.loc[df["neighbourhood"] == nh, "neighbourhood_group"] = most_fequent_group

df.to_csv("airbnb_data_cleaned.csv", index=False)

"""Sample Use Cases"""

if False:
    # 1. What is the average price of a room in each neighbourhood group?
    print("Average price in each neighbourhood group:\n", df.groupby("neighbourhood_group")["price"].mean().round(2))

    # 2. What is the average price of each room type
    print("Average price of each room type:\n", df.groupby("room_type")["price"].mean().round(2))

    # 3. What is the average price of a room in each neighbourhood group, for each room type?
    print("\nAverage price in each neighbourhood group, for each room type:\n", df.groupby(["neighbourhood_group", "room_type"])["price"].mean().round(2))

    # 4. What is the average rating of each neighbourhood group?
    print("\nAverage rating of each neighbourhood group:\n", df.groupby("neighbourhood_group")["review_rate_number"].mean().round(2))

    # 5. What 5 neighbourhood have the most rooms?
    print("\nNeighbourhoods with the most rooms:\n", df["neighbourhood"].value_counts()[:5])