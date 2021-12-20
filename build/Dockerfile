FROM debian:latest

RUN apt-get update && apt-get install -y locales ca-certificates
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8

COPY mock-bot-telegram .

CMD ./mock-bot-telegram
