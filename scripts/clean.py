import pandas as pd
import numpy as np
import os

# ==========================
# Create output folder
# ==========================

os.makedirs("cleaned_data", exist_ok=True)

print("Loading parquet files...")

# ==========================
# Load parquet
# ==========================

flights_df = pd.read_parquet(
    "parquet/flights.parquet"
)

airlines_df = pd.read_parquet(
    "parquet/airlines.parquet"
)

airports_df = pd.read_parquet(
    "parquet/airports.parquet"
)

print("Data loaded successfully!")

# ==========================
# CLEANING 1
# Remove duplicate rows
# ==========================

before_rows = len(flights_df)

flights_df.drop_duplicates(
    inplace=True
)

after_rows = len(flights_df)

print(
    f"Duplicates removed: "
    f"{before_rows - after_rows}"
)

# ==========================
# CLEANING 2
# Fix missing values
# ==========================

delay_cols = [
    "DEPARTURE_DELAY",
    "ARRIVAL_DELAY"
]

for col in delay_cols:
    flights_df[col] = (
        flights_df[col]
        .fillna(0)
    )

# ==========================
# CLEANING 3
# Remove cancelled flights
# ==========================

if "CANCELLED" in flights_df.columns:

    flights_df = flights_df[
        flights_df["CANCELLED"] == 0
    ]

# ==========================
# CLEANING 4
# Remove impossible delays
# ==========================

flights_df = flights_df[
    flights_df["ARRIVAL_DELAY"] > -500
]

flights_df = flights_df[
    flights_df["ARRIVAL_DELAY"] < 1000
]

# ==========================
# CLEANING 5
# String cleanup
# ==========================

flights_df["AIRLINE"] = (
    flights_df["AIRLINE"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ==========================
# CLEANING 6
# Convert date columns
# ==========================

flights_df["FLIGHT_DATE"] = (
    pd.to_datetime(
        flights_df[
            ["YEAR", "MONTH", "DAY"]
        ]
    )
)

# ==========================
# CLEANING 7
# Feature engineering
# Delay category
# ==========================

conditions = [
    flights_df[
        "ARRIVAL_DELAY"
    ] <= 15,

    flights_df[
        "ARRIVAL_DELAY"
    ] <= 60,

    flights_df[
        "ARRIVAL_DELAY"
    ] > 60
]

choices = [
    "On Time",
    "Moderate Delay",
    "High Delay"
]

flights_df[
    "DELAY_CATEGORY"
] = np.select(
    conditions,
    choices,
    default="Unknown"
)

# ==========================
# CLEANING 8
# Create delayed flag
# ==========================

flights_df["IS_DELAYED"] = np.where(
    flights_df[
        "ARRIVAL_DELAY"
    ] > 15,
    1,
    0
)

# ==========================
# CLEANING 9
# Date engineering
# ==========================

flights_df["DAY_NAME"] = (
    flights_df[
        "FLIGHT_DATE"
    ].dt.day_name()
)

flights_df["MONTH_NAME"] = (
    flights_df[
        "FLIGHT_DATE"
    ].dt.month_name()
)

flights_df["QUARTER"] = (
    flights_df[
        "FLIGHT_DATE"
    ].dt.quarter
)

# ==========================
# CLEANING 10
# Optimize memory
# ==========================

flights_df["YEAR"] = (
    flights_df["YEAR"]
    .astype("int16")
)

flights_df["MONTH"] = (
    flights_df["MONTH"]
    .astype("int8")
)

# ==========================
# CLEANING 11
# Merge airline names
# ==========================

flights_df = flights_df.merge(
    airlines_df,
    left_on="AIRLINE",
    right_on="IATA_CODE",
    how="left"
)

# ==========================
# CLEANING 12
# Rename columns
# ==========================

flights_df.rename(
    columns={
        "AIRLINE_y":
        "AIRLINE_NAME"
    },
    inplace=True
)

# ==========================
# Save cleaned data
# ==========================

flights_df.to_parquet(
    "cleaned_data/cleaned_flights.parquet",
    engine="pyarrow",
    compression="snappy",
    index=False
)

print("Cleaning completed!")

print(
    flights_df.shape
)

print(
    flights_df.head()
)