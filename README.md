# Mockerell Telegram Bot

Uses <https://github.com/zoomoid/pymocklib> to run a telegram bot for sounding angry and butthurt on the internet.

## Configuration

Telegram Bots require a token, which you can optain by contacting `@Botfather`. Afterwards, provide your bot token and optionally its name in ENV variables:

```bash
export MOCK_BOT_TOKEN=133769420:notaverysecurebottoken
export MOCK_BOT_NAME=mockerellbot
```

## Running locally

This project uses `pipenv`, a better, more declarative way to interact with python venvs and packages. Get started with

```bash
pip install pipenv
```

Afterwards, you can run

```bash
pipenv install
```

on the source code to get all required dependencies.

Finally, run the bot with `python -m src`.

## Deployment

If you wish to go into the (container) cloud, have a look at [./manifests](./manifests/README.md). It will guide you through the steps of deploying to
Kubernetes. 

If you just wish to run it on Docker, run `docker run -e MOCK_BOT_TOKEN=... ghcr.io/zoomoid/mockerell:latest`.
