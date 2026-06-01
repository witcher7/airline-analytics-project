import pandas as pd 
# === 
# Load Dataset
# ===
flights_df = pd.read_csv("dataset/flights.csv")

airlines_df = pd.read_csv("dataset/airlines.csv")

airports_df = pd.read_csv("dataset/airports.csv")


# ==========================
# Basic Information
# ==========================
print("\n Flights Dataset")
print(flights_df.head())

print("\n Shape")
print(flights_df.shape)

print("\n Columns")
print(flights_df.columns)

print("\n Data Types")
print(flights_df.dtypes)

print("\n Missing Values")
print(flights_df.isnull().sum())

print("\n Duplicate Rows")
print(flights_df.duplicated().sum())

print("\n Statistical Summary")
print(flights_df.describe())



# ==========================
# Airlines Table
# ==========================

print("\n Airlines Dataset")
print(airlines_df.head())

print("\n Airlines Shape")
print(airlines_df.shape)

# ==========================
# Airports Table
# ==========================

print("\n Airports Dataset")
print(airports_df.head())

print("\n Airports Shape")
print(airports_df.shape)