import pandas as pd
import os 

# Create parquet folder if not exists
os.makedirs("parquet", exist_ok=True)
# Load CSV files
flights_df = pd.read_csv("dataset/flights.csv",low_memory=False,dtype={'ORIGIN_AIRPORT': str,'DESTINATION_AIRPORT': str})
airlines_df = pd.read_csv("dataset/airlines.csv")       
airports_df = pd.read_csv("dataset/airports.csv")

# convert to parquet
flights_df.to_parquet("parquet/flights.parquet",engine='pyarrow',compression='snappy', index=False)
airlines_df.to_parquet("parquet/airlines.parquet",engine='pyarrow',compression='snappy', index=False)
airports_df.to_parquet("parquet/airports.parquet",engine='pyarrow',compression='snappy', index=False)
print("Conversion to Parquet completed successfully!")

## TBs To GBs
### GBs to MBs
