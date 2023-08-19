from fastapi.testclient import TestClient

from taxi_data_reporter.s3_storage import list_objects_s3

from .config import settings
from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"app": settings.app_name}


def test_reports_reset():
    response = client.get("/reports/reset")
    objects = list_objects_s3(settings.bucket_name)
    assert response.status_code == 200
    assert len(objects) == 0
