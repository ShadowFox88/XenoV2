FROM python:3.12.8-alpine

ENV POETRY_VIRTUALENVS_CREATE false
ENV PYTHONIOENCODING utf-8

WORKDIR /main

ADD poetry.lock .
ADD pyproject.toml .

RUN apk add --no-cache gcc python3-dev musl-dev linux-headers openssl git bash && rm -rf /var/cache/apk/*

RUN pip install poetry && poetry install --no-root

ADD ./prisma ./prisma
RUN poetry run prisma generate
RUN apk del python3-dev musl-dev linux-headers

ADD . /main

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["poetry run prisma db push --schema prisma/schema.prisma && python main.py"]