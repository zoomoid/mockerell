FROM python:3.10-alpine

RUN apk add --no-cache tini && \
    pip install pipenv

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIPENV_HIDE_EMOJIS=true \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true

WORKDIR /app

COPY docker-entrypoint.sh /bin/

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy --ignore-pipfile

COPY bot bot

ENTRYPOINT [ "/sbin/tini", "--", "docker-entrypoint.sh" ]

CMD [ "python", "-m", "bot" ]
