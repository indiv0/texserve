# texserve #

A server-side utility written in Flask to compile LaTeX files to PDF when triggered by a GitHub post-receive hook.

## Installation ##
### Linux ###

Install [dokku-redis-plugin](https://github.com/luxifer/dokku-redis-plugin) first to provide a database to store information.

    cd /var/lib/dokku/plugins
    git clone https://github.com/luxifer/dokku-redis-plugin redis
    dokku plugins-install

Create the database (server-side):

    dokku redis:create texserve # Server side

Add the remote (client-side):

    git remote add dokku dokku@107.170.59.29:texserve

Install the application:

    virtualenv venv/ --python=python2.7
    source venv/bin/activate
    pip install -r requirements.txt

Run the application locally to test:

    python wsgi.py

Deploy the application to Dokku:

    git push dokku master
