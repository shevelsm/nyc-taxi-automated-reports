import os
from urllib.parse import urlparse

import pandas as pd


class TaxiData:
    def __init__(self, url_pattern: dict, month: str) -> None:
        if self.check_valid_month(month):
            self.month = month
        self.source_url = url_pattern.format(self.month)
        self.filename = os.path.basename(urlparse(self.source_url).path)

    @staticmethod
    def check_valid_month(month: str) -> bool:
        return True

    def is_stored(self) -> bool:
        return False

    def from_source(self) -> int:
        df = pd.read_parquet(self.source_url)
        count = df.shape[0]
        return count

    def from_s3(link: str) -> None:
        pass
