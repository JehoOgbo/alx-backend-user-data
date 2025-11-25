#!/usr/bin/env python3
""" BasicAuth class"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ class to handle basic authentication
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Get the Base64 part of the authorization header for
            a basic authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        try:
            test = authorization_header[0:6] == "Basic "
            if test is False:
                return None
            return authorization_header[6:]
        except Exception as e:
            return None
