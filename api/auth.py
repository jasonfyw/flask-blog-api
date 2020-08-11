from flask import jsonify, make_response
from flask_httpauth import HTTPBasicAuth
import os
from os.path import join, dirname
from dotenv import load_dotenv

auth = HTTPBasicAuth()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

"""
Basic authentication
"""

# basic single-user admin check
@auth.get_password
def get_password(username):
    if username == 'admin':
        return os.environ.get('ADMIN_PASSWORD')
    return None

# handle unauthorised access
@auth.error_handler
def unauthorised():
    return make_response(jsonify({ 'error': 'Unauthorised access'}), 403)

