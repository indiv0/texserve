from flask import Blueprint, request
from flask import jsonify

import json
import time

import subprocess
import os
import tempfile
import shutil

from texserve import InvalidUsage, processLatex

mod = Blueprint('hooks', __name__)


@mod.route('/hooks/post-receive', methods=['POST'])
def getPostReceive():
    # Extract the JSON payload from the request.
    try:
        raw_payload = request.form['payload']
    except KeyError:
        raise InvalidUsage('No payload found')

    # Convert the payload into a JSON format.
    try:
        payload = json.loads(raw_payload)
    except ValueError:
        raise InvalidUsage('Corrupt JSON in payload')

    # Ensure we are tracking the master branch.
    try:
        if payload['ref'] != 'refs/heads/master':
            return ''
    except KeyError:
        raise InvalidUsage('Corrupt payload: missing ref')

    processLatex(payload)

@mod.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
