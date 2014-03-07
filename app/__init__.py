import config
from views import mod

from flask import Flask

import json
import sys

# Initialize the app.
app = Flask(__name__)

# Load the configuration.
app.config.from_pyfile('config.py')

# Register blueprints.
app.register_blueprint(views.mod)
