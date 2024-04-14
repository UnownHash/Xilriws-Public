FROM ubuntu:latest
RUN apt update -y && \
    apt clean

WORKDIR /xilriws

ENV DEBIAN_FRONTEND noninteractive
RUN apt install -y git-all
RUN git clone https://github.com/ccev/xilriws-fingerprint-random.git /xilriws/xilriws-fingerprint-random
RUN git clone https://github.com/ccev/xilriws-cookie-delete.git /xilriws/xilriws-cookie-delete

RUN apt install -y software-properties-common
RUN apt update -y
RUN apt install -y python3 python3-pip
RUN add-apt-repository ppa:savoury1/chromium
RUN apt update && apt install -y chromium-browser

RUN pip install poetry
COPY . .
RUN poetry install

ENTRYPOINT ["poetry", "run", "litestar", "run"]