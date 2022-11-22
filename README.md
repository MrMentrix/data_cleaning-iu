# data_cleaning-iu
Data cleaning task for IU.
Dataset: https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata

## Phase 1 - Getting an overview of the data
# General formatting of columns
- transforming all column names into snake case

# Information about the columns 
- 0 missing values in id and host_id
- few unique values in host_identiy_verified, country, country_code, instant_bookable, cancellation_policy, room_type, review_rate_number, and license

# Columns that may be relevant regarding the goals 
- neighbourhood_group and neighbourhood (for grouping by city districts)
- room_type
- construction_year
- price
- service_fee
- review_rate_number

Also keeping the "id" column for possible use as a foreign key if this data may be used with other data in the future.

## Phase 2 - Normalizing the data
- Transforming all price and service_fee to integers
- Transforming all construction year and review rate number values to integers

## Phase 3 - Removing data / creating a fitting subset
# Dropping selected columns and rows with missing values
- dropping all columns that are not considered to be relevant
- dropping all rows with missing values (1044 rows dropped)

# Looking for outliers
Since one can only really detect numeric outliers, only the numeric columns will be taken into consideration.
- There don't seem to be any outliers in price (50-1200) and service_fee (10-240)
- There don't seem to be any outliers in construction year (2003-2022)

# Looking for semantic errors
- Correcting all spelling mistakes in neighbourhood and neighbourhood_group

# Checking that every neighbourhood only belongs to a single neighbourhood_group

## Phase 4 - Using the data / test cases
# 1. What is the average price of a room in each neighbourhood group?
Bronx            629.89
Brooklyn         626.41
Manhattan        622.50
Queens           630.15
Staten Island    623.87

# 2. What is the average price of each room type
Entire home/apt    624.98
Hotel room         663.56
Private room       625.16
Shared room        633.86

# 3. What is the average price of a room in each neighbourhood group, for each room type?
Bronx                Entire home/apt    622.80
                Private room       636.77
                Shared room        600.26
Brooklyn             Entire home/apt    626.74
                Hotel room         736.12
                Private room       625.75
                Shared room        633.74
Manhattan            Entire home/apt    622.99
                Hotel room         676.44
                Private room       620.79
                Shared room        633.24
Queens               Entire home/apt    627.13
                Hotel room         433.25
                Private room       631.75
                Shared room        643.22
Staten Island        Entire home/apt    640.87
                Private room       603.58
                Shared room        715.60

# 4. What is the average rating of each neighbourhood group?
Bronx            3.33
Brooklyn         3.26
Manhattan        3.28
Queens           3.33
Staten Island    3.41

# 5. What 5 neighbourhood have the most rooms?
Bedford-Stuyvesant    7866
Williamsburg          7693
Harlem                5399
Bushwick              4934
Hell's Kitchen        3933