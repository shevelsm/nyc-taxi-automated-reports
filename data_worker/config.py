from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "NYC Taxi Data Worker"
    url_pattern: str = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{}.parquet"


settings = Settings()
