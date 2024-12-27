import unittest

from app.logic import diff_tags

class Logic(unittest.TestCase):
	def test_no_tag_no_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags=set(),
			has_link=False,
		)
		self.assertEqual('unlinked', add_tag)
		self.assertSetEqual(set(), remove_tags)

	def test_no_tag_with_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags=set(),
			has_link=True,
		)
		self.assertEqual('linked', add_tag)
		self.assertSetEqual(set(), remove_tags)

	def test_unlinked_tag_no_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'unlinked'},
			has_link=False,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual(set(), remove_tags)

	def test_unlinked_tag_with_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'unlinked'},
			has_link=True,
		)
		self.assertEqual('linked', add_tag)
		self.assertSetEqual({'unlinked'}, remove_tags)

	def test_linked_tag_no_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'linked'},
			has_link=False,
		)
		self.assertEqual('orphaned', add_tag)
		self.assertSetEqual({'linked'}, remove_tags)

	def test_linked_tag_with_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'linked'},
			has_link=True,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual(set(), remove_tags)

	def test_orphaned_tag_no_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'orphaned'},
			has_link=False,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual(set(), remove_tags)

	def test_orphaned_tag_with_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'orphaned'},
			has_link=True,
		)
		self.assertEqual('linked', add_tag)
		self.assertSetEqual({'orphaned'}, remove_tags)

	def test_simple_no_tag_no_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags=set(),
			has_link=False,
			single_tag_mode=True,
		)
		self.assertEqual('orphaned', add_tag)
		self.assertSetEqual(set(), remove_tags)

	def test_simple_no_tag_with_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags=set(),
			has_link=True,
			single_tag_mode=True,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual(set(), remove_tags)

	def test_simple_orphaned_tag_no_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'orphaned'},
			has_link=False,
			single_tag_mode=True,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual(set(), remove_tags)

	def test_simple_orphaned_tag_with_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'orphaned'},
			has_link=True,
			single_tag_mode=True,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual({'orphaned'}, remove_tags)

	def test_simple_all_tags_with_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'linked', 'orphaned', 'unlinked'},
			has_link=True,
			single_tag_mode=True,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual({'linked', 'orphaned', 'unlinked'}, remove_tags)

	def test_ignore_match_simple_no_tag_no_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'ignore'},
			has_link=False,
			ignored_tags={'ignore'},
			single_tag_mode=True,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual(set(), remove_tags)

	def test_ignore_match_simple_no_tag_with_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'ignore'},
			has_link=True,
			ignored_tags={'ignore'},
			single_tag_mode=True,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual(set(), remove_tags)

	def test_ignore_match_simple_orphaned_tag_no_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'orphaned', 'ignore'},
			has_link=False,
			ignored_tags={'ignore'},
			single_tag_mode=True,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual({'orphaned'}, remove_tags)

	def test_ignore_match_simple_orphaned_tag_with_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'orphaned', 'ignore'},
			has_link=True,
			ignored_tags={'ignore'},
			single_tag_mode=True,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual({'orphaned'}, remove_tags)

	def test_ignore_match_simple_all_tags_no_link(self):
		(add_tag, remove_tags) = diff_tags(
			torrent_tags={'ignore', 'linked', 'orphaned', 'unlinked'},
			has_link=False,
			ignored_tags={'ignore'},
			single_tag_mode=True,
		)
		self.assertIsNone(add_tag)
		self.assertSetEqual({'linked', 'orphaned', 'unlinked'}, remove_tags)
