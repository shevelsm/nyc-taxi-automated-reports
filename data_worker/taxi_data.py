import os
from urllib.parse import urlparse

import pandas as pd


class TaxiData:
    def __init__(
        self,
        url_pattern: dict,
        lookup_table_url: str,
        s3_url: str,
        month: str,
    ) -> None:
        self.month = month
        self.source_url = url_pattern.format(self.month)
        self.s3_url = s3_url.format(self.month)
        self.filename = os.path.basename(urlparse(self.source_url).path)
        self.lookup_table_url = lookup_table_url

    def collect_from_source(self) -> pd.DataFrame:
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
