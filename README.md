# texserve #

A server-side utility written in Flask to compile LaTeX files to PDF when triggered by a GitHub post-receive hook.

## Installation ##
### Linux ###

Add the remote (client-side):

    git remote add dokku dokku@serverip:texserve

Install the application:

    virtualenv venv/ --python=python2.7
    source venv/bin/activate
    pip install -r requirements.txt

Run the application locally to test:

    python wsgi.py

Configure the application on the server-side:

    dokku config:set texserve AWS_ACCESS_KEY_ID=VALUE1
    dokku config:set texserve AWS_SECRET_ACCESS_KEY=VALUE2
    dokku config:set texserve BUCKET_NAME=VALUE3

Deploy the application to Dokku:

    git push dokku
