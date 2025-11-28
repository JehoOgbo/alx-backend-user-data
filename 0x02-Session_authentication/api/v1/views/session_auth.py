#!/usr/bin/env python3
""" session auth routes
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from os import getenv


@app_views.route('auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ Implement session login route
        POST api/v1/auth_session/login
        receives information to be used for login
    """
    email = request.form.get('email')
    pwd = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if pwd is None or pwd == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if len(user) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if user[0].is_valid_password(pwd) is False:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    sesh = getenv('SESSION_NAME')
    result = jsonify(user[0].to_json())
    result.set_cookie(sesh, session_id)
    return (result)
