FROM ubuntu:latest
RUN apt update -y && \
    apt install -y wget && \
    apt clean

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

WORKDIR /xilriws

COPY . .

ENTRYPOINT ["./xilriws"]