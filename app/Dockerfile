FROM python:3.11 as builder

WORKDIR app

RUN apt-get update && apt-get -y install netcat gcc sqlite3 libsqlite3-dev nano && apt-get clean

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python db/models.py
CMD ["python", "main.py"]



