from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "NYC Taxi Data Worker"
    yellow_taxi_url_pattern: str = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{}.parquet"
    yellow_taxi_data_dict: str = "https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf"
    yellow_taxi_zone_lookup: str = "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
    yellow_taxi_s3_path: str = "yellow_taxi_data/{}.parquet"
    bucket_name: str = "nyc-taxi-reporter-storage"


settings = Settings()
