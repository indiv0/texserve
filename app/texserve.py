import os
import shutil
import tempfile
import subprocess
import time

import json

import config
import s3


def processPayload(payload):
    # JSON stored note information.
    note_data = json.load(open('app/static/notes.json'))

    # Load the file paths and names.
    courses = {}
    try:
        for commit in payload['commits']:
            changed_files = commit['modified'] + commit['added']
            for file in changed_files:
                # Split the filename into the name and the extension (e.g. mat1342a_dgd, tex).
                splitname = file.rpartition('.')
                name = splitname[0]
                extension = splitname[2]

                if extension != 'tex':
                    print('Skipping non-TeX file {}.'.format(file))
                    continue

                try:
                    course = note_data[name]
                except KeyError:
                    print('Could not find the file {} in the documents JSON file.'.format(file))
                    continue

                # Ensure the same commit does not get compiled twice.
                if course['sha'] == commit['id']:
                    print('Refusing to recompile commit for the file {}.'.format(file))
                    continue

                # Update with the info from the new commit.
                print('Updating JSON information for file {} with SHA {} and timestamp {}.'.format(file, commit['id'], commit['timestamp']))
                course['sha'] = commit['id']
                course['timestamp'] = commit['timestamp']

                # Add the course to the list of courses to be re-compiled.
                courses[name] = course
    except KeyError:
        raise InvalidUsage('Corrupt payload - missing one of: commits/modified/added/removed')

    if not courses:
        print('Failed to find any modified LaTeX files to recompile.')
        return ''

    return processLatex(courses, note_data)


def processLatex(courses, note_data):
    try:
        current = os.getcwd()
        print('Creating temporary working directory.')
        temp = tempfile.mkdtemp()
        print('Entering temporary working directory {}.'.format(temp))
        os.chdir(temp)
    except:
        raise InvalidUsage('Failed to setup temporary directory.')

    print('Cloning notes repository')
    git(['clone', 'git@github.com:Indiv0/notes.git'])

    os.chdir('notes')

    for course_name, course in courses.iteritems():
        # Get the path and filename (without suffix) for the tex file.
        print('Compiling {} to PDF.'.format(course_name))
        pdftolatex(course['sha'][:7], getTimeFromTimestamp(course['timestamp']), course_name)

        file_src = course_name + '.pdf'

        if not os.path.exists(file_src):
            print('Failed to compile.')
            continue

        try:
            bucket.uploadFile('{}.pdf'.format(course_name))
        except as e:
            print("Failed to upload compiled PDF to Amazon S3.")
            print(e.error)

        os.chdir(current)
        # Update the JSON data.
        note_data[course_name] = course
        with open(current + '/app/static/notes.json', 'w') as outfile:
            json.dump(note_data, outfile)
            bucket.uploadFile(outfile)

    # Cleanup the temp directory.
    shutil.rmtree(temp)

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
