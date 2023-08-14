import pandas as pd

from .s3_storage import get_df_from_s3_parquet


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
        self.s3_url = f"{s3_url}/{month}.parquet"
        self.lookup_table_url = lookup_table_url

    def __repr__(self) -> str:
        return f"TaxiData ({self.source_url}, {self.lookup_table_url}, {self.count})"

    def __prepare_taxi_df(self) -> None:
        source_data = pd.read_parquet(self.source_url)
        lookup_table = pd.read_csv(self.lookup_table_url)
        self.taxi_df = source_data.merge(
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
        self.taxi_df["pickup_weekday"] = self.taxi_df[
            "tpep_pickup_datetime"
        ].dt.dayofweek
        self.taxi_df["pickup_hour"] = self.taxi_df[
            "tpep_pickup_datetime"
        ].dt.hour

    def collect_from_source(self) -> pd.DataFrame:
        self.__prepare_taxi_df()
        self.count = self.taxi_df.shape[0]
        return self.taxi_df

    def collect_from_s3(self, bucket_name: str) -> pd.DataFrame:
        self.taxi_df = get_df_from_s3_parquet(bucket_name, self.s3_url)
        self.total_count = self.taxi_df.shape[0]
        return self.taxi_df

    def make_jfk_df(self) -> pd.DataFrame:
        self.jfk_df = self.taxi_df.loc[
            (self.taxi_df["Zone_PU"] == "JFK Airport")
            & (self.taxi_df["Zone_DU"] == "JFK Airport")
        ]
        self.jfk_count = self.jfk_df.shape[0]
        return self.jfk_df
