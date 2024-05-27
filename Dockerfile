FROM python:3.11.4-slim AS base

RUN /usr/local/bin/python -m pip install --upgrade pip
WORKDIR /code
COPY requirements.txt requirements.txt

RUN pip install --default-timeout=100 -r requirements.txt

COPY . .

EXPOSE 8088

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:3000"]
