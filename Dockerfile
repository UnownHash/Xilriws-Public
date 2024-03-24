FROM alpine:latest
RUN apk update && apk add --no-cache bash \
        chromium \
        chromium-chromedriver

WORKDIR /xilriws

COPY . .

ENTRYPOINT ["./xilriws"]