from fastapi import FastAPI

from .config import settings
from .s3_storage import get_df_from_s3_parquet, is_on_s3, put_df_to_s3_parquet
from .taxi_data import TaxiData

app = FastAPI()


@app.get("/")
async def root():
    return {"app": settings.app_name}


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "yellow_taxi_url_pattern": settings.yellow_taxi_url_pattern,
        "yellow_taxi_zone_lookup": settings.yellow_taxi_zone_lookup,
    }


@app.get("/report/{month}")
async def report(month: str):
    report_data = TaxiData(
        settings.yellow_taxi_url_pattern,
        settings.yellow_taxi_zone_lookup,
        settings.yellow_taxi_s3_path,
        month,
    )
    if is_on_s3(settings.bucket_name, report_data.s3_url):
        df = get_df_from_s3_parquet(settings.bucket_name, report_data.s3_url)
    else:
        df = report_data.collect_from_source()
        put_df_to_s3_parquet(df, settings.bucket_name, report_data.s3_url)

    return {"shape": df.shape}
