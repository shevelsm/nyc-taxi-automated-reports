FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./taxi_data_reporter /code/app

CMD ["uvicorn", "app.main:app", "--port", "8000"]
