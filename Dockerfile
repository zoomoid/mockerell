FROM python:3.11-alpine

RUN pip install poetry

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry specific settings
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.8.3

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-interaction --no-ansi -vvv

COPY bot bot

USER 65532:65532

CMD [ "python", "-m", "bot" ]
