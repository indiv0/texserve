# texserve #

A server-side utility written in Flask to compile LaTeX files to PDF when triggered by a GitHub post-receive hook.

## Installation ##
### Linux ###

Install the application:

    virtualenv venv/ --python=python2.7
    source venv/bin/activate
    pip install -r requirements.txt

Configure the necessary values in `config.py`.

Run the application:

    python wsgi.py
