import os
from io import BytesIO
from urllib.parse import urlparse

import boto3
import pandas as pd
import pyarrow.parquet as pq

session = boto3.session.Session()
s3 = session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")
s3_resource = boto3.resource(service_name="s3", endpoint_url="https://storage.yandexcloud.net")


class TaxiData:
    def __init__(
        self,
        url_pattern: dict,
        lookup_table_url: str,
        s3_url: str,
        bucket_name: str,
        month: str,
    ) -> None:
        self.month = month
        self.source_url = url_pattern.format(self.month)
        self.s3_url = s3_url.format(self.month)
        self.bucket_name = bucket_name
        self.filename = os.path.basename(urlparse(self.source_url).path)
        self.lookup_table_url = lookup_table_url

    def _collect_from_source(self) -> pd.DataFrame:
        source_data = pd.read_parquet(self.source_url)
        lookup_table = pd.read_csv(self.lookup_table_url)
        return source_data.merge(
            lookup_table,
            how="inner",
            left_on="PULocationID",
            right_on="LocationID",
        ).merge(
            lookup_table,
            how="inner",
            left_on="DOLocationID",
            right_on="LocationID",
            suffixes=("_PU", "_DU"),
        )

    def put_to_s3(self) -> None:
        taxi_data_df = self._collect_from_source()
        out_buffer = BytesIO()
        taxi_data_df.to_parquet(out_buffer, index=False)
        s3.put_object(
            Bucket=self.bucket_name, Key=self.s3_url, Body=out_buffer.getvalue()
        )

    def is_on_s3(self) -> bool:
        for key in s3.list_objects(Bucket=self.bucket_name)['Contents']:
            if key['Key'] == self.s3_url:
                return True
        return False

    def get_from_s3(self) -> pd.DataFrame:
        buffer = BytesIO()
        object = s3_resource.Object(self.bucket_name, self.s3_url)
        object.download_fileobj(buffer)
        df = pq.read_table(buffer)
        return df


'''
[
    {'Key': 'yellow_taxi_data/2023-02.parquet', 'LastModified': datetime.datetime(2023, 8, 10, 17, 59, 15, 16000, tzinfo=tzutc()), 'ETag': '"86db835a94dc54610eb89a97e11c9b63"', 'Size': 62777664, ...}, 
    {'Key': 'yellow_taxi_data/2023-03.parquet', 'LastModified': datetime.datetime(2023, 8, 10, 7, 19, 56, 477000, tzinfo=tzutc()), 'ETag': '"03024534399fa16629b9aa46987b5397"', 'Size': 73764685, ...}
]
'''
