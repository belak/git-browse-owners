import os.path

from flask import render_template, abort
import pygit2

from owner import app
from owner.utils import get_repo, calculate_authors

@app.route('/')
@app.route('/<path:path>')
def browse(path=None):
    repo = get_repo()
    root = repo.head.peel(pygit2.Tree)
    tree = root

    if path is not None:
        path_parts = []
        path, leaf = os.path.split(path)
        while leaf:
            path_parts.append(leaf)
            path, leaf = os.path.split(path)

        if path:
            path_parts.append(path)

        path_parts.reverse()

        try:
            for segment in path_parts:
                oid = tree[segment].id
                tree = repo.get(oid)
        except KeyError:
            abort(404)

        if path_parts:
            path = os.path.join(*path_parts)
        else:
            path = ''
    else:
        path = ''

    dirs, files = calculate_authors(repo, tree, prefix=path)

    return render_template('directory.html', dirs=dirs, files=files)
