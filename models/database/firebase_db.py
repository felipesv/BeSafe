#!/usr/bin/python3
"""
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class Firebase_db:
    """
    """

    __cred = None
    __dburi = None

    def __init__(self):
        """
        create the object connection 
            __cred: credential to connect with firebase
            __dburi: firebase project to connect
            __db: refer to the database
        """
        self.__cred = credentials.Certificate('credentials.json')
        self.__dburi = {'databaseURL': 'https://besafeapp-924d0.firebaseio.com/'}
        self.db = db

    def connect(self):
        """
        create the conecction to database
        """
        firebase_admin.initialize_app(self.__cred, self.__dburi)
