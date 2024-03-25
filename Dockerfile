FROM ubuntu:latest
RUN apt update -y && \
    apt install -y wget && \
    apt clean

WORKDIR /xilriws

RUN apt install -y curl
RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 \
      --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs
RUN npm exec @puppeteer/browsers install chromium@latest
RUN find /xilriws -name "chrome" -exec mv {} /usr/local/bin/chromium \;


COPY . .

CMD ["chromium"]
ENTRYPOINT ["./xilriws"]
