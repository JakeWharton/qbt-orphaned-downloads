FROM alpine:3.24 AS tests

COPY requirements.txt /

RUN apk add --update --no-cache \
      python3 \
      py3-virtualenv \
      py3-pip \
 && rm -rf /var/cache/* \
 && mkdir /var/cache/apk \
 && python3 -m venv .venv \
 && source .venv/bin/activate \
 && pip install --no-cache-dir -r requirements.txt

COPY app /app
COPY etc /etc
COPY test /test
RUN python3 -m unittest discover test


FROM crazymax/alpine-s6:3.23

ENV \
    # Fail if cont-init scripts exit with non-zero code.
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    # Run on the hour by default.
    CRON="0 * * * *" \
    HEALTHCHECK_ID="" \
    HEALTHCHECK_HOST="https://hc-ping.com" \
    QBT_TAG_UNLINKED="Unlinked" \
    QBT_TAG_LINKED="Linked" \
    QBT_TAG_ORPHANED="Orphaned" \
    QBT_IGNORE_TAGS="" \
    QBT_SINGLE_TAG="false" \
    QBT_DELETE_ORPHANS="false" \
    QBT_HOST="localhost:8080" \
    QBT_USER="admin" \
    QBT_PASS="adminadmin" \
    DEBUG=""

COPY requirements.txt /
RUN apk add --update --no-cache \
      curl \
      python3 \
      py3-pip \
      py3-virtualenv \
 && rm -rf /var/cache/* \
 && mkdir /var/cache/apk \
 && python3 -m venv /app/.venv \
 && source /app/.venv/bin/activate \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del \
      py3-pip \
 && true

COPY app /app
COPY etc /etc
