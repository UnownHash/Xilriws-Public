FROM ubuntu:latest
RUN apt update -y && \
    apt clean

RUN apt install -y software-properties-common
RUN add-apt-repository ppa:savoury1/chromium
RUN apt update && apt install -y chromium-browser

WORKDIR /xilriws

COPY . .

ENTRYPOINT ["./xilriws"]
