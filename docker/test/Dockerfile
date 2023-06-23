FROM python:3.10-alpine as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/src

COPY ./requirements/requirements.txt /app/requirements.txt

RUN apk add --update --no-cache --virtual .tmp-deps \
    build-base linux-headers && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/python-deps/wheels -r /app/requirements.txt && \
    apk del .tmp-deps


FROM python:3.10-alpine3.18 as tester

LABEL MAINTAINER="Hso | safarnejad.ho@gmail.com"
ENV PYTHONUNBUFFERD 1

COPY .env /app/.env
COPY scripts /app/scripts
COPY src /app/src

WORKDIR /app/src

RUN apk update && apk add libc-dev gcc

COPY --from=builder /app/python-deps/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/* && \
    chmod -R +x /app/scripts

ENV PATH="/app/scripts:$PATH"

CMD ["test.sh"]

