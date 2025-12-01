#!/usr/bin/env python3
""" Flask app
"""
from flask import jsonify, Flask, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def hello_world():
    """ Entry endpoint into app
        Usage:
            GET /
        Return a simple json
    """
    return jsonify({'message': 'Bienvenue'})

@app.route('/users', methods=['POST'], strict_slashes=False)
def create_users():
    """ Endpoint to create User objects

      - Expects email and password
      - Usage:
            POST /users -d {"email": "haha@gpa.com", "password": "***"}
    """
    if request:
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            new_user = AUTH.register_user(email, password)
            return jsonify({"email": new_user.email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400
    return jsonify({"error": "missing fields"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

