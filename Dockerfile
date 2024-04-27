FROM ubuntu:latest
RUN apt update -y && \
    apt clean

WORKDIR /xilriws
ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y
RUN apt install curl
RUN curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"| tee /etc/apt/sources.list.d/brave-browser-release.list
RUN apt update -y
RUN apt install -y brave-browser

COPY . .

ENTRYPOINT ["./xilriws"]