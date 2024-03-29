qBittorrent Orphaned Downloads
==============================

Maintains a tag on torrents whose files have no hardlinks outside the download directory.
Also maintains a text file of all paths which are unowned by any torrent.

This tool is provided as a Docker container which runs as a cron job.

[![Docker Image Version](https://img.shields.io/docker/v/jakewharton/qbt-orphaned-downloads?sort=semver)][hub]
[![Docker Image Size](https://img.shields.io/docker/image-size/jakewharton/qbt-orphaned-downloads)][layers]

 [hub]: https://hub.docker.com/r/jakewharton/qbt-orphaned-downloads/
 [layers]: https://microbadger.com/images/jakewharton/qbt-orphaned-downloads


Usage
-----

The container connects to qBittorrent over its API which is exposed the same way as its web interface.
You will need a valid username and password.
The default username is 'admin', and the default password is 'adminadmin' which reflect the qBittorrent defaults.

There are three general ways to connect:

 1. Use the qBittorrent container as the network for this container.
 2. Use the qBittorrent container hostname.
 3. Use an explicit hostname/IP that resolves to the container.

Option 2 and option 3 are really the same thing and are the recommended path.

For option 2, ensure your qBittorrent container has a hostname defined.
For `docker run` this means specifying `--hostname qbittorrent`.
For Docker Compose use the `hostname` key in the service definition:
```yaml
services:
  qbittorrent:
    image: linuxserver/qbittorrent
    hostname: qbittorrent
    # …
```

Start this container and point it at your qBittorrent instance with the `QBT_HOST` environment variable.
Mount your downloads folder at `/downloads`.
Unowned files will be written to `/data/unowned.txt` which you can optionally mount or simply look at inside the container's filesystem.

```
$ docker run -d \
    -e "QBT_HOST=http://qbittorrent:8080" \
    -v /path/to/downloads:/downloads \
    -v /path/to/data:/data \  # Optional
    jakewharton/qbt-orphaned-downloads:1
```

For Docker Compose, add it as an additional service:
```yaml
services:
  qbt-orphaned-downloads:
    container_name: qbt-orphaned-downloads
    image: jakewharton/qbt-orphaned-downloads:1
    restart: unless-stopped
    volumes:
      - /path/to/downloads:/downloads
      - /path/to/data:/data  # Optional
    environment:
      - "QBT_HOST=http://qbittorrent:8080"
```

If you have a non-default username or password, specify the `QBT_USER` and/or `QBT_PASS` environment variables, respectively.

The container will check all of your torrents every hour by default.
To change when it runs, specify the `CRON` environment variable with a valid cron specifier.
For help creating a valid cron specifier, visit [cron.help][cron].

 [cron]: https://cron.help/#*/5_*_*_*_*

The 'Orphaned' tag will be used by default.
To change it, specify your desired tag name in the `QBT_TAG` environment variable.

Tags can be used to prevent specific torrents from being marked as orphans. Specify one or more tags in the
`QBT_IGNORE_TAGS` as a comma-separated list.

To be notified when sync is failing visit https://healthchecks.io, create a check, and specify
the ID to the container using the `HEALTHCHECK_ID` environment variable.


LICENSE
======

MIT. See `LICENSE.txt`.

    Copyright 2020 Jake Wharton
