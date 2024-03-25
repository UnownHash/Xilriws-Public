FROM python:3.9-slim
RUN apt update -y && \
    apt clean && \
    pip install poetry

WORKDIR /maltelogin

RUN apt install -y software-properties-common
RUN add-apt-repository ppa:savoury1/chromium
RUN apt update && apt install -y chromium-browser

COPY app.py .
COPY ptc_auth.py .
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install

ENTRYPOINT ["poetry", "run", "litestar", "run"]