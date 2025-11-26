#!/usr/bin/env python3
""" BasicAuth class"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


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

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Get the user object from credentials
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            user = User.search({'email': user_email})
        except Exception as e:
            return None
        if len(user) <= 0:
            return None
        if user[0].is_valid_password(user_pwd):
            return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        auth_header = self.authorization_header(request)
        extracted_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(extracted_header)
        user_email, password = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_email, password)
