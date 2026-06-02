import pandas as pd
import os
import time

from sqlalchemy import create_engine
from dotenv import load_dotenv

# ======================
# Load ENV
# ======================

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

# ======================
# DB Connection
# ======================

connection_string = (
    f"postgresql://"
    f"{username}:"
    f"{password}@"
    f"{host}:"
    f"{port}/"
    f"{database}"
)

engine = create_engine(
    connection_string,
    pool_pre_ping=True
)

# ======================
# Load parquet
# ======================

print("Loading parquet...")

df = pd.read_parquet(
    "cleaned_data/cleaned_flights.parquet"
)

print(
    f"Original rows: {len(df)}"
)

# ======================
# TEST LOAD
# ======================

df = df.head(500000)

print(
    f"Testing rows: {len(df)}"
)

# ======================
# Upload chunks
# ======================

chunk_size = 50000

start = time.time()

for i in range(
    0,
    len(df),
    chunk_size
):

    chunk = df.iloc[
        i:i + chunk_size
    ]

    print(
        f"Uploading "
        f"{i} -> "
        f"{i + len(chunk)}"
    )

    chunk.to_sql(
        name="fact_flights",
        con=engine,
        if_exists=(
            "replace"
            if i == 0
            else "append"
        ),
        index=False,
        method="multi",
        chunksize=5000
    )

print(
    f"Finished in "
    f"{round(time.time()-start,2)} sec"
)