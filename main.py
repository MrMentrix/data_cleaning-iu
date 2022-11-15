import pandas as pd

data = pd.read_csv("airbnb_data.csv")

# renaming all columns into one snake case
data.columns = data.columns.str.lower().str.replace(" ", "_")

# relevant columns
relevant_columns = ["id", "neighbourhood_group", "neighbourhood", "room_type", "construction_year", "price", "service_fee", "review_rate_number"]

# getting the subset of the data, with only the relevant columns
df = data[relevant_columns]

# dropping all rows with missing values
df = df.dropna()

# set all prices to be integers, removing all "$" and "," characters. This will throw a FutureWarning, but it's ok
df["price"] = df["price"].str.replace("$", "").str.replace(",", "").astype(int)
df["service_fee"] = df["service_fee"].str.replace("$", "").str.replace(",", "").astype(int)

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