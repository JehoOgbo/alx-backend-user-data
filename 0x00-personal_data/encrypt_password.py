#!/usr/bin/env python3
import bycrypt


def hash_password(password: str) -> bytes | bytearray:
    """ Hash a password
    """
    salt = bycrypt.gensalt(rounds=12)

    hashed_password = bycrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def is_valid(hashed_password: bytes | bytearray, password: str) -> bool:
    """ Checks if a password matches the hashed_password
    """
    return bycrypt.checkpw(password.encode('utf-8'), hashed_password)
