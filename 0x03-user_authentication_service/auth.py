#!/usr/bin/env python3
""" auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError , NoResultFound


def _hash_password(password: str) -> bytearray:
    """ Hash the given password
        and return the Hash
    """
    bytespw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytespw, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Hash password and save new user to the database
        """
        if email is None or email == '':
            raise ValueError('No email given')
        if password is None or password == '':
            raise ValueError('No password given')

        email_dict = {'email': email}
        try:
            user = self._db.find_user_by(**email_dict)
            if user:
                raise ValueError(f"User {email} already exists")
        except (NoResultFound, InvalidRequestError) as e:
            pwd = _hash_password(password)
            return self._db.add_user(email, password)
