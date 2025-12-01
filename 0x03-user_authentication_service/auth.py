#!/usr/bin/env python3
""" auth module
"""
import bcrypt
from db import DB
from uuid import uuid4
from user import User
from sqlalchemy.exc import InvalidRequestError , NoResultFound


def _hash_password(password: str) -> bytearray:
    """ Hash the given password
        and return the Hash
    """
    bytespw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytespw, salt)

def _generate_uuid() -> str:
    """ Return a string representation of a unique identifier
    """
    return str(uuid4())


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
            return self._db.add_user(email, pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """ Verify that a user exists with the given email and
            password
        """
        if email and password:
            try:
                email_dict = {"email": email}
                user = self._db.find_user_by(**email_dict)
                if user:
                    pass_bytes = password.encode('utf-8')
                    if bcrypt.checkpw(pass_bytes, user.hashed_password):
                        return True
                    return False
            except Exception as e:
                return False
        return False

    def create_session(self, email: str) -> str:
        """ Find the user corresponding to the email,
            generate a unique identifier and store that as the session id
            Return the session id
        """
        if email:
            email_dict = {'email': email}
            try:
                user = self._db.find_user_by(**email_dict)
                if user:
                    iden = _generate_uuid()
                    update_dict = {"session_id": iden}
                    self._db.update_user(user.id, **update_dict)
                    return iden
            except Exception as e:
                return None
        return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Get the user attached to a session
        """
        if session_id:
            try:
                sesh_dict = {'session_id': session_id}
                user = self._db.find_user_by(**sesh_dict)
                return user
            except Exception as e:
                return None
        return None
