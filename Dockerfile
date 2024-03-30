FROM ubuntu:latest
RUN apt update -y && \
    apt clean

WORKDIR /xilriws
ENV DEBIAN_FRONTEND noninteractive

RUN apt install -y git-all
RUN git clone https://github.com/ccev/xilriws-fingerprint-random.git /maltelogin/xilriws-fingerprint-random
RUN git clone https://github.com/ccev/xilriws-cookie-delete.git /maltelogin/xilriws-cookie-delete

RUN apt install -y software-properties-common
RUN add-apt-repository ppa:savoury1/chromium
RUN apt update && apt install -y chromium-browser

COPY . .

ENTRYPOINT ["./xilriws"]