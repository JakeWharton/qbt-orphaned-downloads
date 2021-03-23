FROM oznu/s6-alpine:3.12

ENV \
    # Fail if cont-init scripts exit with non-zero code.
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    # Run on the hour by default.
    CRON="0 * * * *" \
    HEALTHCHECK_ID="" \
    HEALTHCHECK_HOST="https://hc-ping.com" \
    QBT_TAG="Orphaned" \
    QBT_IGNORE_TAGS="" \
    QBT_HOST="localhost:8080" \
    QBT_USER="admin" \
    QBT_PASS="adminadmin" \
    DEBUG=""

COPY requirements.txt /
RUN apk add --update --no-cache python3 curl \
 && rm -rf /var/cache/* \
 && mkdir /var/cache/apk \
 && ln -sf python3 /usr/bin/python \
 && python -m ensurepip \
 && pip3 install --no-cache-dir --upgrade pip \
 && pip3 install --no-cache-dir -r requirements.txt

COPY root/ /
