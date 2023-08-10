from fastapi import FastAPI

from .config import settings
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
        settings.bucket_name,
        month,
    )
    report_data.put_to_s3()
    return {"dtypes": report_data.s3_url}
