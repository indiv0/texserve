from app import config
from app import views

from flask import Flask

# Initialize the app.
app = Flask(__name__)

# Load the configuration.
app.config.from_pyfile('config.py')

# Register blueprints.
app.register_blueprint(views.mod)

# Create a representation of the S3 bucket.
bucket = s3.Bucket(config.BUCKET_NAME, config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY)
