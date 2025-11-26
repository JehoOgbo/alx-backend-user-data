#!/usr/bin/env python3
""" Auth class """
from flask import request
from typing import List, TypeVar
from os import getenv



class Auth:
    """ Template for authentication systems
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if path is not in the list of paths excluded_paths
        otherwise returns False
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ returns the value of the request header authorization
          - returns None if non-existent
          - request is a flask request object
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header:
            return header
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None
          - request will be a flask request object
            to be implemented in child classes
        """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request
        """
        if request is None:
            return None
        cookie_name = getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
