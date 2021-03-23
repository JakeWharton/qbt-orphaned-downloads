#!/usr/bin/python3 -u

import os
from qbittorrentapi import Client

DEBUG = os.environ['DEBUG'] == 'true'

DOWNLOADS_PATH = "/downloads"

if DEBUG:
	print('Creating inode mappings...')

# Create a map of all downloaded files to their stats (specifically, inode and link count).
file_to_stats = dict()
for dir_path, _, file_names in os.walk(DOWNLOADS_PATH):
	for file_name in file_names:
		full_path = os.path.join(dir_path, file_name)
		relative_path = os.path.relpath(full_path, DOWNLOADS_PATH)
		file_to_stats[relative_path] = os.stat(full_path)

# Reverse file-to-inode map into an inode-to-count map. A file may be hardlinked multiple times in the download
# directory so a local count is needed to determine if the total count contains external references.
inode_to_count = dict()
for file, stats in file_to_stats.items():
	inode_to_count[stats.st_ino] = inode_to_count.get(stats.st_ino, 0) + 1


TAG = os.environ['QBT_TAG']
IGNORE_TAGS = filter(None, os.environ['QBT_IGNORE_TAGS'].split(','))
HOST = os.environ['QBT_HOST']
USER = os.environ['QBT_USER']
PASS = os.environ['QBT_PASS']

client = Client(host=HOST, username=USER, password=PASS)

for torrent in client.torrents.info():
	if DEBUG:
		print('---', torrent.name, '---')
		print('Tags:', torrent.tags)

	orphaned = True
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

		# Determine is this file is an orphan by looking for hardlinks outside of the download directory.
		download_links = inode_to_count[stats.st_ino]
		has_external_links = (stats.st_nlink - download_links) > 0
		if DEBUG:
			print(file.name, stats.st_ino, stats.st_nlink, download_links, has_external_links)
		if has_external_links:
			orphaned = False
			break

	if DEBUG:
		print('Orphaned?', orphaned)

	torrent_tags = torrent.tags.split(', ')
	has_ignore_tag = any(tag in IGNORE_TAGS for tag in torrent_tags)

	if orphaned and not has_ignore_tag:
		if TAG not in torrent_tags:
			print('Tagging', torrent.name)
			torrent.addTags(TAG)
	else:
		if TAG in torrent_tags:
			print('Clearing', torrent.name)
			torrent.removeTags(TAG)
