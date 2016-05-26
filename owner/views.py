import os.path

from flask import render_template, request
import pygit2

from owner import app
from owner.utils import get_node

@app.route('/')
@app.route('/<path:path>')
def browse(path=None):
    node = get_node(app.repo, path)

    if request.args.get('recurse', False):
        dirs = node.dir_authors
    else:
        dirs = node.dir_no_authors

    files = node.file_authors
    return render_template('directory.html', dirs=dirs, files=files)
