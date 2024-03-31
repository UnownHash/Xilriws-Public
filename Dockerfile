FROM ubuntu:latest
RUN apt update -y && \
    apt clean

WORKDIR /xilriws
ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:savoury1/chromium
RUN apt update && apt install -y chromium-browser

COPY . .

ENTRYPOINT ["./xilriws"]