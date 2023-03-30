FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update -y && \
    # apt-get install -y build-essential && \
    pip install -r requirements.txt

ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]