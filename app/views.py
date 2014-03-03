from flask import Blueprint, request
from flask import jsonify

import json
import time

import subprocess
import os
import tempfile
import shutil

mod = Blueprint('hooks', __name__)


@mod.route('/hooks/post-receive', methods=['POST'])
def getPostReceive():
    payload = getPayload(request)

    # Ensure we are tracking the master branch.
    try:
        if payload['ref'] != 'refs/heads/master':
            return ''
    except KeyError:
        raise InvalidUsage('Corrupt payload: missing ref')

    # JSON stored note information.
    note_data = json.load(open('tranquill/static/notes.json'))

    # Load the file paths and names.
    courses = {}
    try:
        for commit in payload['commits']:
            changed_files = commit['modified'] + commit['added']
            for file in changed_files:
                # Path and filename: e.g. /dgd/fall2013/ and mat1341a_dgd.tex
                path, filename = os.path.split(file)
                # Filename without filetype suffix: e.g. mat1341a_dgd
                filename = filename.rpartition('.')[0]

                try:
                    course = note_data[filename]
                except KeyError:
                    continue

                # Ensure the same commit does not get compiled twice.
                if course['sha'] == commit['id']:
                    continue

                # Update with the info from the new commit.
                course['sha'] = commit['id']
                course['timestamp'] = commit['timestamp']

                # Add the course to the list of courses to be re-compiled.
                courses[filename] = course
    except KeyError:
        raise InvalidUsage('Corrupt payload - missing one of: commits/modified/added/removed')

    try:
        current = os.getcwd()
        temp = tempfile.mkdtemp()
        os.chdir(temp)
    except:
        raise InvalidUsage('Failed to setup temporary directory.')

    git(['clone', 'git@github.com:Indiv0/notes.git'])

    for course_name, course in courses.iteritems():
        try:
            os.chdir(temp)
        except IOError:
            print("Failed to cd into temporary directory.")

        # Get the path and filename (without suffix) for the tex file.
        type = course['course']['type'].lower()
        term = course['course']['term'].lower().replace(' ', '')
        path = type + '/' + term + '/'

        try:
            os.chdir('notes/' + path)
        except IOError:
            print("Failed to cd into tex file directory.")

        pdftolatex(course['sha'][:7], getTimeFromTimestamp(course['timestamp']), course_name)

        file_src = temp + '/notes/' + path + '/' + course_name + '.pdf'

        if not os.path.exists(file_src):
            print('Failed to compile.')
            continue

        target = current + '/tranquill/static/dl/'

        if not os.path.exists(target):
            os.makedirs(target)

        try:
            shutil.copy(file_src, target + course_name + '.pdf')
        except:
            print("Failed to copy compiled PDF to destination.")

        # Update the JSON data.
        note_data[course_name] = course
        os.chdir(current)
        with open('tranquill/static/notes.json', 'w') as outfile:
            json.dump(note_data, outfile)

    # Cleanup the temp directory.
    shutil.rmtree(temp)

    os.chdir(current)

    return ''


def pdftolatex(sha, time, name):
    compile_command = 'pdflatex -interaction=batchmode -halt-on-error "\def\sha{' + sha + '} \def\commitDateTime{' + time + '} \input{' + name + '.tex}"'

    # Compile the file into a PDF.
    print('Compiling: ' + name + '.tex')
    subprocess.call(compile_command, shell=True)
    # Compile again to ensure references are correct.
    subprocess.call(compile_command, shell=True)


def git(args):
    args = ['git'] + args
    git = subprocess.Popen(args, stdout=subprocess.PIPE)
    details = git.stdout.read()
    details = details.strip()
    return details


def getPayload(request):
    try:
        raw_payload = request.form['payload']
    except KeyError:
        raise InvalidUsage('No payload found')

    try:
        return json.loads(raw_payload)
    except ValueError:
        raise InvalidUsage('Corrupt JSON in payload')


def getTimeFromTimestamp(time_string):
    gmt_offset_seconds = -3 * 60 * 60

    timestamp = time.strptime(time_string[:-6], '%Y-%m-%dT%H:%M:%S')

    localtime = time.localtime(time.mktime(timestamp) - gmt_offset_seconds)
    return time.strftime("%Y-%m-%d-T%H:%M:%S", localtime)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@mod.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
