import os 
import boto3
# boto3 is a module that provides an interface to interact with AWS services, including S3.

BUCEKT_NAME = "airlineprojectsystem2026"

s3 = boto3.client('s3')
files = {
    "parquet/flights.parquet": "raw/flights/flights.parquet",
    "parquet/airlines.parquet": "raw/airlines/airlines.parquet",
    "parquet/airports.parquet": "raw/airports/airports.parquet",
}
print("Uploading files to S3 bucket...")
for local_path, s3_path in files.items():
    s3.upload_file(local_path, BUCEKT_NAME, s3_path)
    print(f"Uploaded {local_path} to s3://{BUCEKT_NAME}/{s3_path}")

print("All files uploaded successfully.")