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
RUN pip install poetry --break-system-packages

RUN apt install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub > linux_signing_key.pub
RUN install -D -o root -g root -m 644 linux_signing_key.pub /etc/apt/keyrings/linux_signing_key.pub
RUN sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/linux_signing_key.pub] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
RUN apt update -y
RUN apt install -y google-chrome-stable

#RUN apt install -y curl
#RUN curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
#RUN echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"| tee /etc/apt/sources.list.d/brave-browser-release.list
#RUN apt update -y
#RUN apt install -y brave-browser

COPY . .
RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "app.py"]