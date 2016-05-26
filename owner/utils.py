from collections import defaultdict
import os.path

from cached_property import cached_property
from flask import abort
import pygit2

from owner import app


def get_repo():
    return pygit2.Repository(app.config['REPO_PATH'])


def splitall(path):
    allparts = []
    while True:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])

    if allparts and not allparts[-1]:
        allparts.pop()

    return allparts


class TreeNode(object):
    def __init__(self, repo, path):
        self.repo = repo
        self.path = path
        if self.path is None:
            self.path = ''

        self.components = splitall(self.path)

        self.tree = repo.head.peel(pygit2.Tree)
        if self.path is not None:
            try:
                for segment in self.components:
                    oid = self.tree[segment].id
                    self.tree = self.repo.get(oid)
            except KeyError:
                abort(404)
                return
        else:
            self.path = ''


    @cached_property
    def entries(self):
        dirs = []
        files = []
        for entry in self.tree:
            if entry.type == 'tree':
                dirs.append(entry)
            elif entry.type == 'blob':
                files.append(entry)

        return dirs, files

    def dir_no_authors(self):
        dirs = []

        dir_entries, _ = self.entries
        for d in dir_entries:
            path = os.path.join(self.path, d.name)

            dirs.append((path, []))

        return sorted(dirs)

    def dir_authors(self):
        dirs = []

        dir_entries, _ = self.entries
        for d in dir_entries:
            authors = defaultdict(lambda: 0)
            path = os.path.join(self.path, d.name)

            inner_tree = TreeNode(self.repo, path)
            inner_dir_authors = inner_tree.dir_authors()
            inner_file_authors = inner_tree.file_authors()

            for _, author_info in inner_dir_authors:
                for author, count in author_info:
                    authors[author] += count

            for _, author_info in inner_file_authors:
                for author, count in author_info:
                    authors[author] += count

            dirs.append((path, sorted(authors.items(), key=lambda k: -k[1])))

        return sorted(dirs)


    def file_authors(self):
        files = []

        _, file_entries = self.entries
        for f in file_entries:
            authors = defaultdict(lambda: 0)
            path = os.path.join(self.path, f.name)
            blame = self.repo.blame(path)
            for hunk in blame:
                author = hunk.orig_committer.name
                authors[author] += hunk.lines_in_hunk

            files.append((path, sorted(authors.items(), key=lambda k: -k[1])))

        return sorted(files)
