from flask import Blueprint, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
import os
from dotenv import load_dotenv, find_dotenv
from itsdangerous import (TimedJSONWebSignatureSerializer as Serialiser, BadSignature, SignatureExpired)

auth = HTTPBasicAuth()

load_dotenv(find_dotenv())

"""
Basic token-based authentication
"""

# authenticate based on credentials/token
@auth.verify_password
def verify_password(username_or_token, password):
    # first check token passed in as username
    user = verify_auth_token(username_or_token)

    # else check username/password credentials
    if not user:
        if not username_or_token == 'admin' or not password == os.environ.get('ADMIN_PASSWORD'):
            return False
    return True

# handle unauthorised access
@auth.error_handler
def unauthorised():
    return make_response(jsonify({ 'error': 'Unauthorised access'}), 403)


"""
Token generation and verification
"""

# generate new token 
def generate_auth_token(_id, expiration = 6000):
    s = Serialiser(os.environ.get('SECRET_KEY'), expires_in = expiration)
    return s.dumps({ 'id': _id })

# check if token is valid
def verify_auth_token(token):
    s = Serialiser(os.environ.get('SECRET_KEY'))
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
    return jsonify({ 'user': 'admin' })


"""
Protected endpoint to fetch token
"""

token = Blueprint('token', __name__)

@token.route('/token')
@auth.login_required
def get_auth_token():
    token = generate_auth_token('admin')
    return jsonify({ 'token': token.decode('ascii') })

