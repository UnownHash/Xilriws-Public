FROM ubuntu:latest
RUN apt update -y && \
    apt clean

WORKDIR /maltelogin

RUN apt install -y software-properties-common
RUN apt install -y python3 python3-pip
RUN add-apt-repository ppa:savoury1/chromium
RUN apt update && apt install -y chromium-browser

RUN pip install poetry
COPY app.py .
COPY ptc_auth.py .
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install

ENTRYPOINT ["poetry", "run", "litestar", "run"]