import os.path

import pygit2

from owner import app


def get_repo():
    return pygit2.Repository(app.config['REPO_PATH'])

def calculate_authors(repo, tree, prefix=''):
    dirs = []
    files = []

    for entry in tree:
        path = os.path.join(prefix, entry.name)
        if entry.type == 'tree':
            authors = {}
            inner_tree = repo.get(entry.id)
            inner_dirs, inner_files = calculate_authors(repo, inner_tree, prefix=path)

            for name, author_info in inner_dirs:
                for author, count in author_info:
                    if author not in authors:
                        authors[author] = 0

                    authors[author] += count

            for name, author_info in inner_files:
                for author, count in author_info:
                    if author not in authors:
                        authors[author] = 0

                    authors[author] += count

            dirs.append((path, sorted(authors.items(), key=lambda x: -x[1])))

        elif entry.type == 'blob':
            files.append((path, blob_authors(repo, path)))

    return dirs, files

def blob_authors(repo, path):
    authors = {}
    blame = repo.blame(path)
    for hunk in blame:
        author = hunk.orig_committer.name
        if author not in authors:
            authors[author] = 0

        authors[author] += hunk.lines_in_hunk

    return sorted(authors.items(), key=lambda author: -author[1])
