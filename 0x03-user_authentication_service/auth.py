#!/usr/bin/env python3
""" auth module
"""
import bcrypt


def _hash_password(password: str) -> bytearray:
    """ Hash the given password
        and return the Hash
    """
    bytespw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytespw, salt)
