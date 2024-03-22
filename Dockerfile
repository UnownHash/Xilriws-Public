FROM python:3.11-slim
RUN apt update -y && \
    apt install -y chromium-driver && \
    apt clean && \
    pip install poetry

WORKDIR /app
COPY . .
RUN poetry install

ENTRYPOINT ["poetry", "run", "litestar", "run"]
