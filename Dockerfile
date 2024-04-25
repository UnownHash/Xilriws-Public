FROM ubuntu:latest
RUN apt update -y && \
    apt clean

WORKDIR /xilriws

ENV DEBIAN_FRONTEND noninteractive
RUN apt install -y git-all
RUN git clone https://github.com/UnownHash/Xilriws-Public
RUN cp -r Xilriws-Public/xilriws-fingerprint-random /xilriws/xilriws-fingerprint-random
RUN cp -r Xilriws-Public/xilriws-cookie-delete /xilriws/xilriws-cookie-delete
RUN cp -r Xilriws-Public/xilriws-proxy /xilriws/xilriws-proxy

RUN apt install -y software-properties-common
RUN apt update -y
RUN apt install -y python3 python3-pip
# RUN add-apt-repository ppa:savoury1/chromium
# RUN apt update && apt install -y chromium-browser
RUN apt install curl
RUN curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"| tee /etc/apt/sources.list.d/brave-browser-release.list
RUN apt update -y
RUN apt install -y brave-browser

RUN pip install poetry
COPY . .
RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "app.py"]