from io import BytesIO

import boto3
import pandas as pd
import pyarrow.parquet as pq
from botocore.config import Config

config = Config(
   retries={
      'max_attempts': 10,
      'mode': 'standard'
   }
)

session = boto3.session.Session()
s3 = session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net", config=config)
s3_resource = boto3.resource(service_name="s3", endpoint_url="https://storage.yandexcloud.net")


def put_df_to_s3_parquet(taxi_data_df: pd.DataFrame, bucket: str, key: str) -> None:
    out_buffer = BytesIO()
    taxi_data_df.to_parquet(out_buffer, index=False)
    s3.put_object(
        Bucket=bucket, Key=key, Body=out_buffer.getvalue()
    )


def is_on_s3(bucket: str, key: str) -> bool:
    for key in s3.list_objects(Bucket=bucket)['Contents']:
        if key['Key'] == key:
            return True
    return False


def get_df_from_s3_parquet(bucket: str, key: str) -> pd.DataFrame:
    buffer = BytesIO()
    object = s3_resource.Object(bucket, key)
    object.download_fileobj(buffer)
    df = pq.read_table(buffer)
    return df


'''
[
    {'Key': 'yellow_taxi_data/2023-02.parquet', 'LastModified': datetime.datetime(2023, 8, 10, 17, 59, 15, 16000, tzinfo=tzutc()), 'ETag': '"86db835a94dc54610eb89a97e11c9b63"', 'Size': 62777664, ...}, 
    {'Key': 'yellow_taxi_data/2023-03.parquet', 'LastModified': datetime.datetime(2023, 8, 10, 7, 19, 56, 477000, tzinfo=tzutc()), 'ETag': '"03024534399fa16629b9aa46987b5397"', 'Size': 73764685, ...}
]
'''
