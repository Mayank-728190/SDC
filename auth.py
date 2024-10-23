from flask import request, jsonify
from functools import wraps

def check_auth(username, password):
    return username == 'admin' and password == 'secret'

def authenticate():
    return jsonify({"message": "Authentication Required"}), 401

def requires_auth(f):
    @wraps(f)  # Preserve the original function's name and docstring
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated