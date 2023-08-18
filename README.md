# NYC Taxi Reporter

## Description

It's a simple web application for creating basic analytic reports based on [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

Examples of the final reports:

- [2020-03.pdf](https://github.com/shevelsm/nyc-taxi-automated-reports/blob/master/examples/2020-03.pdf)
- [2023-02.pdf](https://github.com/shevelsm/nyc-taxi-automated-reports/blob/master/examples/2023-02.pdf)

### Tools

Used tools in the project:

- python
- fastapi
- uvicorn
- pydantic
- pandas
- pyarrow
- boto3
- matplotlib
- seaborn
- pytest
- httpx

Dependecy managment tools used for development:

- pyenv
- poetry

### Features

- Enhancing the data for better visualizing;
- Store echanced dataframe compactly in parquet format in s3 storage and use it as a cache for a faster response.

## Run project

Before start the project the s3 credentials should be created should be obtained. Here you can find how to obtain it for Yandex Cloud storage -
[Setting up AWS tools](https://cloud.yandex.com/en-ru/docs/ydb/docapi/tools/aws-setup).

### Locally (poetry)

Set aws envs or place it at the specific files - [more about that](https://cloud.yandex.com/en-ru/docs/storage/tools/boto#setup)

After configuration run the commands below in the projects directory:

``` bash
poetry install
poetry run uvicorn taxi_data_reporter.main:app --port 8000 --reload
```

### Docker

Also it can run in Docker using `Dockerfile``. Build and run container with the commands below:

``` bash
docker build -t nyc-taxi-reporter:latest .
docker run -e AWS_ACCESS_KEY_ID={your_key_id} -e AWS_SECRET_ACCESS_KEY={your_access_key} nyc-taxi-reporter:latest
```

### Testing

To run fastapi tests use pytest in the project directory:

``` bash
pytest
```

## Endpoints

After starting a web server it's time to describe its endpoints. This is the list of all endpoint with description of its fuctionality:

1. `/` - just return the name of the app;
2. `/readme` - redirect user to this README file with the instructions and desctiption;
3. `/data_dict` - redirect user to the description of the intial dataset fields;
4. `/report/{month}` - main endpoint for obtaining reports using **month** variable. Month format is `%Y-%m` like **2023-06**.  Finally it leads to the pdf report (see examples) that stored in s3 bucket;
5. `/report/data/{month}` - returns info for prepared dataset for final reporting;
6. `/reports` - list of report files in s3 storage;
7. `/reports/reset` - reset all report data in the precofigured bucket;

## Futher plans

- Input data validation (month, bucket_name and etc);
- More tests for fastapi and s3 communications with corner cases;
- Ability to use additional GET parametrs to configure a final report.
