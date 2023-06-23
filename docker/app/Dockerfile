FROM python:3.10-alpine as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/src

COPY ./requirements/requirements.txt /app/requirements.txt

RUN apk add --update --no-cache --virtual .tmp-deps \
    build-base linux-headers && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/python-deps/wheels -r /app/requirements.txt && \
    apk del .tmp-deps


FROM python:3.10-alpine3.18 as runner

LABEL MAINTAINER="Hso | safarnejad.ho@gmail.com"
ENV PYTHONUNBUFFERD 1

COPY .env /app/.env
COPY scripts /app/scripts
COPY src /app/src

WORKDIR /app/src

RUN apk update && apk add libc-dev gcc && \
    python3 -m venv /app/.venv

COPY --from=builder /app/python-deps/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN /app/.venv/bin/pip install --no-cache /wheels/* && \
    # creating non-root user for limited permissions
    adduser --disabled-password --no-create-home appuser && \
    # creating static and media dirs and giving access for R/W to the appuser
    mkdir -p /app/vol/web/static && \
    mkdir -p /app/vol/web/media && \
    chown -R appuser: /app/vol && \
    chmod -R 755 /app/vol && \
    chmod -R +x /app/scripts

# adding python environment from /.venv to the path
# now-on any python command will use /.venv python interpreter
ENV PATH="/app/scripts:/app/.venv/bin:$PATH"
# switching root user to appuser
# the appuser does not have full access
USER appuser

CMD ["run.sh"]

