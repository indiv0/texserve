from app import config
from app import views

from flask import Flask

# Initialize the app.
app = Flask(__name__)

# Load the configuration.
app.config.from_object('config.DevelopmentConfig')

# Register blueprints.
app.register_blueprint(views.mod)
