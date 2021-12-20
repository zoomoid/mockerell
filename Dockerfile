FROM fpco/stack-build:latest AS builder

WORKDIR /srv

COPY . .

RUN rm stack.yaml.lock && \
    apt update -y && \
    apt upgrade -y && \
    stack build && \
    cp $(stack path --local-install-root)/bin/mock-bot-telegram .

FROM debian:latest

RUN apt-get update && apt-get install -y locales ca-certificates
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8

COPY --from=builder /srv/mock-bot-telegram /usr/local/bin/

CMD ["mock-bot-telegram"]
