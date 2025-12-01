#!/usr/bin/env python3
""" Flask app
"""
from flask import jsonify, Flask, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def hello_world() -> str:
    """ Entry endpoint into app
        Usage:
            GET /
        Return a simple json
    """
    return jsonify({'message': 'Bienvenue'})

@app.route('/users', methods=['POST'], strict_slashes=False)
def create_users() -> str:
    """ Endpoint to create User objects

      - Expects email and password
      - Usage:
            POST /users -d 'email=bob@bob.com' -d 'password=mySuperPwd'
    """
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            new_user = AUTH.register_user(email, password)
            return jsonify({"email": new_user.email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400
    return jsonify({"error": "missing fields"}), 400

@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Endpoint to login (create a new session)

      - Expects email and password fields
      - Usage:
            POST /sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd'
    """
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        if AUTH.valid_login(email, password):
            sesh_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", sesh_id)
            return response
        abort(401)

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def log_out() -> str:
    """ Endpoint to logout (destroy a session)

        Usage:
            DELETE /sessions session_id=idijf833-idjo-fkjd-kdfjkjf
      - Expects session_id as a set_cookie
      - Find the user with requested session id.
      - If exists, destroy and redirect to GET /
        - else abort 403
    """
    if request.method == 'DELETE':
        sesh_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(sesh_id)
        if user is None:
            abort(403)
        AUTH.destroy_session(user.id)
        return redirect("/")




if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

