FROM python:3.10.5-alpine3.16

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ENV PORT=80

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT