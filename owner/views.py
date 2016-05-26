import os.path

from flask import render_template
from interruptingcow import timeout
import pygit2

from owner import app
from owner.utils import TreeNode

@app.route('/')
@app.route('/<path:path>')
def browse(path=None):
    node = TreeNode(app.repo, path)

    try:
        # Because this is a recursive operation, it can be painfully expensive
        with timeout(10, exception=RuntimeError):
            dirs = node.dir_authors()
    except:
        dirs = node.dir_no_authors()

    files = node.file_authors()
    return render_template('directory.html', dirs=dirs, files=files)
