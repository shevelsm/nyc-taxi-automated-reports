from fastapi import FastAPI

from .config import settings
from .taxi_data import TaxiData

app = FastAPI()
URL_PATTERN = str(settings.url_pattern)


@app.get("/")
async def root():
    return {"app": settings.app_name}


@app.get("/report/{month}")
async def report(month: str):
    report_data = TaxiData(URL_PATTERN, month)
    count = report_data.from_source()
    return {"count": count}


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "url_pattern": settings.url_pattern,
    }
