FROM python:3.9-alpine

COPY . /app

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["gunicorn",  "--bind", "0.0.0.0:8000", "application:create_app()"]
