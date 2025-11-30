#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, attributes
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError , NoResultFound
# from sqlalchemy.orm.exc import NoResultFound

from user import Base
from user import User
from typing import Dict


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Create a new user and add it to the database
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)

            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs: Dict) -> User:
        """ Finds a user based on a set of filters
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return user

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """ Updates a user object
        """
        session = self._session
        dictionary = {"id": user_id}
        user = self.find_user_by(**dictionary)
        if user:
            for key, value in kwargs.items():
                attributes.set_attribute(user, key, value)

            session.commit()
        else:
            return None
