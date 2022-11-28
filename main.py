import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import itertools
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder

# reading the (original) data
df = pd.read_csv("airbnb_data.csv")

# REFERENCE: "2.2 Exploring the Data"
# renaming all columns into one snake_case format
df.columns = df.columns.str.lower().str.replace(" ", "_")
# saves a renamed version of the original data so working with it is a bit easier
# df.to_csv("airbnb_data_renamed.csv", index=False)

# REFERENCE: "2.2.1 Redundant Features"
# dropping all columns that don't provide any useful information
df.drop(labels=["license", "house_rules", "country", "country_code"], axis=1, inplace=True)

# REFERENCE: "2.2.2 Impossible Value Ranges" | visualization/minimum_nights.py for visualization code | figures/minimum_nights.png for figure
# putting all values of minimum_nights into the range of 1-30
df["minimum_nights"] = df["minimum_nights"].apply(lambda x: 1 if x < 1 else 30 if x > 30 else x)
# putting all values of availability_365 into the range of 0-365
df["availability_365"] = df["availability_365"].apply(lambda x: 0 if x < 0 else 365 if x > 365 else x)
# putting all values of calculated_host_listings_count into the range of 0-10
df["calculated_host_listings_count"] = df["calculated_host_listings_count"].apply(lambda x: 0 if x < 0 else 10 if x > 10 else x)

# REFERENCE: "2.2.3 Mixed Data Types"
# converting all values of price and service_fee to floats
df["price"] = df["price"].str.replace("$", "").str.replace(",", "").astype(float)
df["service_fee"] = df["service_fee"].str.replace("$", "").str.replace(",", "").astype(float)

# REFERENCE: "2.2.4 Duplicate Data Records"
# removing all duplicate rows, based on apartment ID
df.drop_duplicates(subset=["id"], inplace=True)

# REFERENCE: "2.2.5 Typograhical errors"
# calculating the similarity ratio between all neighbourhood values
# use itertools.combinations to get all combinations of neighbourhoods
if False: # set to True for usage
    subset = "neighbourhood_group"
    combinations = list(itertools.combinations(df.dropna(subset=[subset])[subset].unique(), 2))
    for combination in combinations:
        ratio = SequenceMatcher(None, combination[0], combination[1]).ratio()
        if ratio > 0.75:
            print(f"Similarity ratio between {combination[0]} and {combination[1]} is {ratio}")

# correcting the neighbourhood names
df["neighbourhood_group"] = df["neighbourhood_group"].str.replace("brookln", "Brooklyn")
df["neighbourhood_group"] = df["neighbourhood_group"].str.replace("manhatan", "Manhattan")

# REFERENCE: "2.3.1 Missing Neighbhourhood Values"

# impute the missing values of "neighbourhood" by KNN imputation based on "long" and "lat"

# encoding all labels in neighbourhood to integers
label_encoder = LabelEncoder()
# encode all neighbourhood values that are not NaN
df["neighbourhood"] = df["neighbourhood"].fillna("NaN")
df["neighbourhood"] = label_encoder.fit_transform(df["neighbourhood"])

# imputing missing values
imputer = KNNImputer(n_neighbors=5)
df[["neighbourhood", "long", "lat"]] = imputer.fit_transform(np.array(df[["neighbourhood", "long", "lat"]]))
df["neighbourhood"] = label_encoder.inverse_transform(df["neighbourhood"].astype(int))

# ensuring that every single neighbourhood only refers to one neighbourhood group
for nh in df["neighbourhood"].unique():
    if len(df[df["neighbourhood"] == nh]["neighbourhood_group"].unique()) > 1:
        most_frequent_group = df[df["neighbourhood"] == nh]["neighbourhood_group"].value_counts().index[0]
        # print("\n", nh, df[df["neighbourhood"] == nh]["neighbourhood_group"].unique())
        df.loc[df["neighbourhood"] == nh, "neighbourhood_group"] = most_frequent_group

# REFERENCE: "2.3.2 Missing Review Data"
# dropping features because of too many missing data and no possible imputation
df.drop(labels=["last_review", "reviews_per_month"], axis=1, inplace=True)
df["review_rate_number"].fillna(df["review_rate_number"].mode(), inplace=True)

# REFERENCE: "2.3.3 Other missing Data"
# fill all missing values of name
df["name"].fillna(f"Apartment in {df['neighbourhood']}", inplace=True)

# fill all missing values of host_name and host_identitiy_verified
df["host_name"].fillna("Unknown", inplace=True)
df["host_identity_verified"].fillna("unconfirmed", inplace=True)

# fill all missing values of instant_bookable, default to False
df["instant_bookable"].fillna(False, inplace=True)

# fill all missing values of cancellation_policy, default to "moderate"
df["cancellation_policy"].fillna("moderate", inplace=True)

# fill all missing values of construction_year by a SUBJECTIVE(!), arbitrary default value of 2000
df["construction_year"].fillna(2000, inplace=True)

# fill all missing price and service_fee values based on their neighbourhood
for nh in df["neighbourhood"].unique():
    df.loc[(df["neighbourhood"] == nh) & (df["price"].isna()), "price"] = round(df[df["neighbourhood"] == nh]["price"].mean())
    df.loc[(df["neighbourhood"] == nh) & (df["service_fee"].isna()), "service_fee"] = round(df[df["neighbourhood"] == nh]["service_fee"].mean())

# fill all missing minimum_nights values with 1 (happens to be the mode)
df["minimum_nights"].fillna(1, inplace=True)

# fill all missing number_of_reviews values with 0, assuming there were no reviews.
df["number_of_reviews"].fillna(0, inplace=True)
df["review_rate_number"].fillna(3, inplace=True)

# fill all missing availability_365 values with 0
df["availability_365"] = df["availability_365"].fillna(0)

# fill all missing calculated_host_listings_count values with 1
df["calculated_host_listings_count"] = df["calculated_host_listings_count"].fillna(1)

df.to_csv("airbnb_data_cleaned.csv", index=False) # saving the cleaned data to a new csv file

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