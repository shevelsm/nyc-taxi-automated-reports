from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "NYC Taxi Data Reporter"
    readme: str = "https://github.com/shevelsm/nyc-taxi-automated-reports/blob/master/README.md"
    data_dict_url: str = "https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf"
    yellow_taxi_url_pattern: str = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{}.parquet"
    yellow_taxi_data_dict: str = "https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf"
    yellow_taxi_zone_lookup: str = "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
    yellow_taxi_s3_path: str = "yellow_taxi_data"
    yellow_taxi_s3_reports: str = "yellow_taxi_data/pdf_reports"
    bucket_name: str = "nyc-taxi-reporter-storage"


settings = Settings()
