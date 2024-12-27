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

To be notified when sync is failing visit https://healthchecks.io, create a check, and specify
the ID to the container using the `HEALTHCHECK_ID` environment variable.

### Tagging

By default, three tags are maintained: 'Unlinked', 'Linked', and 'Orphaned'.
Unlinked torrents have never been linked.
Orphaned torrents have been previously linked.
This can be used to detect things like newer versions, season packs, etc. as opposed to those which just have not been matched properly.

All three tags can be changed using the `QBT_TAG_UNLINKED`, `QBT_TAG_LINKED`, and `QBT_TAG_ORPHANED` environment variables, respectively.

Alternatively, for a simpler tagging scheme, setting `QBT_SINGLE_TAG=true` will only tag things as 'Orphaned' (using `QBT_TAG_ORPHANED`) when unlinked, and clear that tag when linked.

Tags can be used to prevent specific torrents from being marked by this tool.
Specify one or more tags in the `QBT_IGNORE_TAGS` as a comma-separated list.

If you would like torrents marked as orphaned to be automatically deleted on the next run, set `QBT_DELETE_ORPHANS=true` environment variable.
This feature does not work in single-tag mode.
**WARNING**: This will perform data deletion in an unattended manner.
Do not use this option if you value your data.
Every effort has been made to ensure correctness, but please use additional mechanisms which will allow you to recover if something goes horribly wrong (e.g., automatic timed ZFS snapshots).
You have been warned!


LICENSE
======

MIT. See `LICENSE.txt`.

    Copyright 2020 Jake Wharton
