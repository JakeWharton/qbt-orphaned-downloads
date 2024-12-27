from typing import Optional

def diff_tags(
	torrent_tags: set[str],
	has_link: bool,
	tag_unlinked: str = 'unlinked',
	tag_linked: str = 'linked',
	tag_orphaned: str = 'orphaned',
	ignored_tags: set[str] = frozenset(),
	single_tag_mode: bool = False,
) -> tuple[Optional[str], set[str]]:
	"""
	Diff `torrent_tags` against `has_link`, `ignored_tags`, and `single_tag_mode` to determine
	changes which need made in the form of an optional new tag to add and a set of tags to remove.

	:param torrent_tags: Set of existing tags on the torrent.
	:param has_link: True if the torrent contains a linked file.
	:param tag_unlinked: Name of tag for 'unlinked' state.
	:param tag_linked: Name of tag for 'linked' state.
	:param tag_orphaned: Name of tag for 'orphaned' state.
	:param ignored_tags: Set of tags to match which indicate a torrent should be ignored.
	:param single_tag_mode: Only set 'orphaned' state or nothing, rather than ternary state tags.
	:return: `(add_tag, remove_tags)` tuple of `Optional[str]` and `set[str]`, respectively.
	"""

	next_tag: Optional[str] = None
	existing_tags: set[str] = torrent_tags & {tag_unlinked, tag_linked, tag_orphaned}

	if not torrent_tags.isdisjoint(ignored_tags):
		pass # Ignored. Just remove any tags we know about.

	elif has_link:
		if not single_tag_mode:
			next_tag = tag_linked

	elif single_tag_mode or tag_linked in existing_tags or tag_orphaned in existing_tags:
		next_tag = tag_orphaned

	else:
		next_tag = tag_unlinked

	# Only remove tags which do not reflect the desired tag.
	if next_tag and next_tag in existing_tags:
		existing_tags.remove(next_tag)
		next_tag = None

	return next_tag, existing_tags
