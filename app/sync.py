import os
from qbittorrentapi import Client, TorrentStates
from logic import diff_tags

DEBUG = os.environ['DEBUG'] == 'true'

DOWNLOADS_PATH = "/downloads"
INELIGIBLE_STATES = {
	TorrentStates.QUEUED_DOWNLOAD,
	TorrentStates.DOWNLOADING,
	TorrentStates.ALLOCATING,
	TorrentStates.MOVING,
	TorrentStates.PAUSED_DOWNLOAD,
	TorrentStates.STALLED_DOWNLOAD,
}

if DEBUG:
	print('Creating inode mappings...')

# Create a map of all downloaded files to their stats (specifically, inode and link count).
file_to_stats = {}
for dir_path, _, file_names in os.walk(DOWNLOADS_PATH):
	for file_name in file_names:
		full_path = os.path.join(dir_path, file_name)
		relative_path = os.path.relpath(full_path, DOWNLOADS_PATH)
		file_to_stats[relative_path] = os.stat(full_path)

# Copy all relative paths to a set which we can mutate as we traverse the torrent list.
unowned_relative_paths = set(file_to_stats.keys())

# Reverse file-to-inode map into an inode-to-count map. A file may be hardlinked multiple times in the download
# directory so a local count is needed to determine if the total count contains external references.
inode_to_count = {}
for file, stats in file_to_stats.items():
	inode_to_count[stats.st_ino] = inode_to_count.get(stats.st_ino, 0) + 1


TAG_UNLINKED: str = os.environ['QBT_TAG_UNLINKED']
TAG_LINKED: str = os.environ['QBT_TAG_LINKED']
TAG_ORPHANED: str = os.environ['QBT_TAG_ORPHANED']
ALL_TAG_SET: set[str] = {TAG_UNLINKED, TAG_LINKED, TAG_ORPHANED}
IGNORE_TAG_SET: set[str] = set(filter(None, os.environ['QBT_IGNORE_TAGS'].split(',')))
SINGLE_TAG_MODE: bool = os.environ['QBT_SINGLE_TAG'] == 'true'
DELETE_ORPHANS: str = os.environ['QBT_DELETE_ORPHANS']
HOST = os.environ['QBT_HOST']
USER = os.environ['QBT_USER']
PASS = os.environ['QBT_PASS']

if DELETE_ORPHANS and SINGLE_TAG_MODE:
	raise Exception("Orphan deletion cannot be used in single-tag mode")

client = Client(host=HOST, username=USER, password=PASS)

for torrent in client.torrents.info():
	torrent_tags: set[str] = set(torrent.tags.split(', '))
	if DEBUG:
		print('---', torrent.name, '---')
		print('Tags:', torrent_tags)
		print('State:', torrent.state_enum)

	# Regardless of torrent state, remove all paths known by the torrent.
	for file in torrent.files:
		if file.name in unowned_relative_paths:
			unowned_relative_paths.remove(file.name)

	if torrent.state_enum in INELIGIBLE_STATES:
		if DEBUG:
			print("Ineligible!")
		continue

	if DELETE_ORPHANS and TAG_ORPHANED in torrent_tags:
		if not DEBUG:
			print('[{}]'.format(torrent.name), end=' ')
		if DELETE_ORPHANS == 'true':
			print("Deleting orphan!")
			client.torrents_delete(torrent.info.hash, delete_files=True)
		elif DELETE_ORPHANS == 'log':
			print("Would delete orphan!")

	has_link = False  # Assume orphaned unless proven otherwise.
	for file in torrent.files:
		if file.priority == 0:
			if DEBUG:
				print(file.name, "Ignored (priority == 0)")
			continue  # This file is not set to download. Ignore.
		if file.progress < 1:
			if DEBUG:
				print(file.name, "Ignored (progress < 1)")
			continue  # This file is not completed and may not have been linked. Ignore.

		if file.name not in file_to_stats:
			if DEBUG:
				print(file.name, "Ignored (stats missing)")
			continue  # Torrent was added after we checked the filesystem. Ignore.
		stats = file_to_stats[file.name]

		# Determine is this file is an orphan by looking for hardlinks outside the download directory.
		download_links = inode_to_count[stats.st_ino]
		has_external_links = (stats.st_nlink - download_links) > 0
		if DEBUG:
			print(file.name, stats.st_ino, stats.st_nlink, download_links, has_external_links)
		if has_external_links:
			has_link = True
			break

	if DEBUG:
		print('Linked?', has_link)

	(add_tag, remove_tags) = diff_tags(
		torrent_tags=torrent_tags,
		has_link=has_link,
		tag_unlinked=TAG_UNLINKED,
		tag_linked=TAG_LINKED,
		tag_orphaned=TAG_ORPHANED,
		ignored_tags=IGNORE_TAG_SET,
		single_tag_mode=SINGLE_TAG_MODE,
	)

	if remove_tags:
		if not DEBUG:
			print('[{}]'.format(torrent.name), end=' ')
		print('Removing tag(s)', remove_tags)
		torrent.remove_tags(remove_tags)
	if add_tag:
		if not DEBUG:
			print('[{}]'.format(torrent.name), end=' ')
		print('Adding tag', add_tag)
		torrent.add_tags(add_tag)

print('Done')
print()
print('Found', len(unowned_relative_paths), 'unowned files in download directory')
if not os.path.exists('/data'):
	os.mkdir('/data')
with open('/data/unowned.txt.temp', 'w') as w:
	for unowned_relative_path in sorted(unowned_relative_paths):
		w.write(unowned_relative_path)
		w.write('\n')
os.rename('/data/unowned.txt.temp', '/data/unowned.txt')
