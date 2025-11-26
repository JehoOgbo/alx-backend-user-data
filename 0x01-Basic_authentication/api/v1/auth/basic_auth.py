#!/usr/bin/env python3
""" BasicAuth class"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ class to handle basic authentication
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decode the base 64 in the authorization header
            to get the encoded information
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            result = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
            return result.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Get the user email and password from the decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':')
        return email, password
