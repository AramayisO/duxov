FROM python:3.9

WORKDIR /usr/src

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./tests ./tests
COPY ./pytest.ini ./pytest.ini

EXPOSE 8000