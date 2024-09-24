FROM python:3.10.12
LABEL authors="nilhalil"

RUN apt-get update && apt-get install -y python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /server/
RUN pip install -r /server/requirements.txt

COPY ./models /server/models
COPY ./api_v1__warehouse /server/api_v1__warehouse
COPY config.py /server/
COPY main.py /server/
COPY .env /server/

WORKDIR /server

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5010", "--reload"]
