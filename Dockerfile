FROM ubuntu:latest
RUN apt update -y && \
    apt install -y chromium-driver && \
    apt clean

WORKDIR /xilriws

COPY . .

ENTRYPOINT ["./xilriws"]