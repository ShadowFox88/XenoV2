FROM python:3.12.8-alpine

ENV POETRY_VIRTUALENVS_CREATE false
ENV PYTHONIOENCODING utf-8

WORKDIR /main

ADD poetry.lock .
ADD pyproject.toml .
ADD ./prisma ./prisma

RUN apk add --no-cache gcc \ 
    python3-dev \ 
    musl-dev \
    linux-headers \
    openssl \
    git \
    bash \
    # Remove Cache
    && rm -rf /var/cache/apk/* \
    # Install Requirements
    && pip install poetry \
    && poetry install --no-root \
    # Generate Prisma Files
    && poetry run prisma generate \
    # Remove Cache
    && rm -rf /root/.cache/prisma \
    && rm -rf /root/.cache/prisma-python/nodeenv \
    && rm -rf /root/.npm/ \
    && rm -rf /root/.cache/pip \
    && rm -rf /root/.cache/pypoetry \
    && apk del python3-dev musl-dev linux-headers openssl

ADD . /main

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["python main.py"]