from io import BytesIO

import boto3
import pandas as pd
import pyarrow.parquet as pq
from botocore.config import Config

config = Config(retries={"max_attempts": 10, "mode": "standard"})

session = boto3.session.Session()
s3_client = session.client(
    service_name="s3", endpoint_url="https://storage.yandexcloud.net", config=config
)
s3_resource = boto3.resource(
    service_name="s3", endpoint_url="https://storage.yandexcloud.net"
)


def put_to_s3(obj: BytesIO, bucket_name: str, key: str) -> None:
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=obj.getvalue())


def check_key_on_s3(bucket_name: str, check_key: str) -> bool:
    try:
        keys = s3_client.list_objects(Bucket=bucket_name)["Contents"]
    except KeyError:
        print("It's my fault!")
        return False
    for key in keys:
        if key["Key"] == check_key:
            return True
    return False


def get_df_from_s3_parquet(bucket_name: str, key: str) -> pd.DataFrame:
    buffer = BytesIO()
    object = s3_resource.Object(bucket_name, key)
    object.download_fileobj(buffer)
    df = pq.read_table(buffer).to_pandas()
    return df


def clear_s3_storage(bucket_name: str) -> None:
    bucket = s3_resource.Bucket(bucket_name)
    bucket.objects.all().delete()


def get_s3_url(bucket_name: str, key: str) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket_name,
            "Key": key,
        },
    )
