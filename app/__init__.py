from app import config
from app import views

from flask import Flask

import json

# Initialize the app.
app = Flask(__name__)

# Load the configuration.
app.config.from_pyfile('config.py')

# Register blueprints.
app.register_blueprint(views.mod)

# Create a representation of the S3 bucket.
bucket = s3.Bucket(config.BUCKET_NAME, config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY)

# Load JSON stored note information.
print('Loading JSON data on notes from file.')
note_data = json.load(open('notes.json'))
# Retrieve 'notes.json' from the bucket, and write it if it doesn't exist.
try:
    note_data = bucket.getFile('notes.json')
except:
    print('Uploading updated JSON data on notes to S3 bucket.')
    bucket.uploadFile('notes.json')
