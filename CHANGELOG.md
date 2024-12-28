# Changelog

## [Unreleased]
[Unreleased]: https://github.com/JakeWharton/qbt-orphaned-downloads/compare/2.0.3...HEAD


## [2.0.3] - 2024-12-27
[2.0.3]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/2.0.3

### Fixed

 * Do not crash if `DEBUG` or `QBT_IGNORE_TAGS` env vars are not specified.


## [2.0.2] - 2024-12-27
[2.0.2]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/2.0.2

### Fixed

 * Re-add `curl` dependency to the Docker container for Healthchecks.io integration.


## [2.0.1] - 2024-12-27
[2.0.1]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/2.0.1

### Fixed

 * Torrent deletion now actually works (only if enabled!)


## [2.0.0] - 2024-12-27
[2.0.0]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/2.0.0

The tool now maintains three tags instead of just one.
This allows differentiating never-linked (unlinked) from those which used to be linked but are no longer (orphaned).
See the `README.md` for more info.

**NOTE**: Upgrading from 1.x will leave the "Orphaned" tag in place.
If you want to start with a clean slate, right-click the "Orphaned" tag and select "Remove tag".
This will cause all unlinked torrents to show as "Unlinked" after the next run.

To revert to the previous behavior of 1.x, set `QBT_SINGLE_TAG=true` environment variable.
This will only toggle the "Orphaned" tag on or off.

If you would like torrents marked as orphaned to be automatically deleted on the next run, set `QBT_DELETE_ORPHANS=true` environment variable.
This feature does not work in single-tag mode.
**WARNING**: This will perform data deletion in an unattended manner.
Do not use this option if you value your data.
Every effort has been made to ensure correctness, but please use additional mechanisms which will allow you to recover if something goes horribly wrong (e.g., automatic timed ZFS snapshots).
You have been warned!

### Fixed

 * Properly support different save paths for torrents. The tool still assumes there is a single base folder that can be mounted at `/downloads`, but any custom or category save paths on a torrent will be respected.


## [1.3.0] - 2021-07-21
[1.3.0]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/1.3.0

### Added

 * Track files in download directory which are unowned by any torrent. List is written to `/data/unowned.txt`.


## [1.2.1] - 2021-04-18
[1.2.1]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/1.2.1

### Changed

 * Add stalled state to ignored states.


## [1.2.0] - 2021-04-17
[1.2.0]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/1.2.0

### Changed

 * Do not mark a torrent as an orphan if it is in a downloading or queued state.


## [1.1.0] - 2021-03-23
[1.1.0]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/1.1.0

### Added

 * `QBT_IGNORE_TAGS` comma-separated list of tags which will be ignored when considering a torrent an orphan.


## [1.0.2] - 2021-03-09
[1.0.2]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/1.0.2

No code changes. The automatic release script was updated to push multiple tags
and to mirror to GitHub's container registry.


## [1.0.1] - 2021-02-23
[1.0.1]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/1.0.1

### Fixed

 * Properly parse tags on torrents with multiple tags set.


## [1.0.0] - 2020-12-24
[1.0.0]: https://github.com/JakeWharton/qbt-orphaned-downloads/releases/tag/1.0.0

Initial release
