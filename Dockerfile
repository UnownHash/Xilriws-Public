FROM ubuntu:latest
RUN apt update -y && \
    apt clean

WORKDIR /xilriws
ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y
RUN apt install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub > linux_signing_key.pub
RUN install -D -o root -g root -m 644 linux_signing_key.pub /etc/apt/keyrings/linux_signing_key.pub
RUN sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/linux_signing_key.pub] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
RUN apt update -y
RUN apt install -y google-chrome-stable

COPY . .

ENTRYPOINT ["./xilriws"]