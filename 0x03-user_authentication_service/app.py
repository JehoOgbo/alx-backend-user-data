#!/usr/bin/env python3
""" Flask app
"""
from flask import jsonify, Flask
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

