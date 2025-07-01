FROM python:3.13

WORKDIR app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV WORKERS=1

ENV PORT=8008
ENV HOST=0.0.0.0
ENV UVICORN_ARGS "core.setup:setup --host $HOST --port $PORT --workers $WORKERS"

# Settings for PostgresSQL database connections
ENV POSTGRES_DB=""
ENV POSTGRES_USER=""
ENV POSTGRES_PASSWORD=""
ENV POSTGRES_HOST="host.docker.internal"
ENV POSTGRES_PORT=""
ENV POSTGRES_SCHEMA=""

COPY app .

RUN echo "Внимание: не забудьте указать актуальные переменные среды для подключения к базе данных Postgresql".
RUN echo "Пример запуска контейнера: docker run --rm -it -p 5432:5432 -e POSTGRES_DB=test_db -e POSTGRES_USER=test_user -e POSTGRES_PASSWORD=test_pass -e -e POSTGRES_PORT=5432 POSTGRES_SCHEMA=postgres myapp"

RUN pip install --upgrade pip  --no-cache-dir
COPY requirements.txt .
RUN pip install -r requirements.txt


CMD uvicorn $UVICORN_ARGS
