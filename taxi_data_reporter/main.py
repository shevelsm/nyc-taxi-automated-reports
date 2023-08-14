from fastapi import FastAPI
from fastapi.background import BackgroundTasks
from fastapi.responses import RedirectResponse

from .config import settings
from .s3_storage import (
    clear_s3_storage,
    put_df_to_s3_parquet,
    check_key_on_s3
)
from .taxi_data import TaxiData

app = FastAPI()
bucket_name = settings.bucket_name


@app.get("/")
async def root():
    return {"app": settings.app_name}


@app.get("/readme")
async def readme():
    return RedirectResponse(url=settings.readme)


@app.get("/data_dict")
async def data_dict():
    return RedirectResponse(url=settings.data_dict_url)


@app.get("/report/{month}")
async def make_report(month: str, background_tasks: BackgroundTasks):
    report_data = TaxiData(
        settings.yellow_taxi_url_pattern,
        settings.yellow_taxi_zone_lookup,
        settings.yellow_taxi_s3_path,
        month,
    )
    if check_key_on_s3(bucket_name, report_data.s3_url):
        taxi_df = report_data.collect_from_s3(bucket_name)
    else:
        taxi_df = report_data.collect_from_source()
        background_tasks.add_task(put_df_to_s3_parquet, taxi_df, bucket_name, report_data.s3_url)
    return {"sample": taxi_df.sample().to_dict()}


@app.get("/report/data/{month}")
async def report_data(month: str):
    report_data = TaxiData(
        settings.yellow_taxi_url_pattern,
        settings.yellow_taxi_zone_lookup,
        settings.yellow_taxi_s3_path,
        month,
    )
    if check_key_on_s3(bucket_name, report_data.s3_url):
        return {"info": report_data}
    else:
        return {"info": f"The report data for {month} is not prepared. Run report/{month}"}


@app.get("/reports")
async def reports():
    return {"reports": list()}


@app.get("/report_data/reset")
async def report_data_reset(background_tasks: BackgroundTasks):
    background_tasks.add_task(clear_s3_storage, settings.bucket_name)
    return {"message": "All report_data have been removed from s3 storage"}
