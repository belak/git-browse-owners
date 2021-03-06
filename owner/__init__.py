from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

app.nodes = {}

from owner.utils import get_repo
app.repo = get_repo()

import owner.views
