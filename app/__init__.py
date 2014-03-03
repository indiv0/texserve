import config
import views

from flask import Flask

# Initialize the app.
app = Flask(__name__)

# Load the configuration.
app.config.from_pyfile('config.py')
app.secret_key = config.SECRET_KEY

# Register blueprints.
app.register_blueprint(views.mod)
