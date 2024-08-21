FROM ubuntu:latest
RUN apt update -y && \
    apt clean

WORKDIR /xilriws
ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y
RUN apt install -y wget
RUN wget -q -O - https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_125.0.6422.141-1_amd64.deb > ./chrome.deb
RUN apt install -y ./chrome.deb
RUN rm ./chrome.deb

COPY . .

ENTRYPOINT ["./xilriws"]