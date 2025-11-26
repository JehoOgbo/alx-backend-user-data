#!/usr/bin/env python3
""" SessionAuth class"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ Define functions that implement session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a new session id for the user
        """
        if user_id is None or type(user_id) is not str:
            return None
        iden = str(uuid4())
        self.user_id_by_session_id[iden] = user_id
        return iden

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get the user_id attached to a session_id
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)
