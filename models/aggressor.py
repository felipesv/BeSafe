#!/usr/bin/python3
"""
Aggressor class
"""
from models import storage
from uuid import uuid4


class Aggressor:
    """
    """

    aggressorRefer = storage.db.reference('aggressor')

    def __init__(self, *args, **kwargs):
        """
        args: create aggressor object
            0: description or name
        kwargs: create an object aggressor with data from db
        """
        self._referDb = None
        self._aggressorDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Aggressor.valid_args(args):
            self._idAggressor = str(uuid4())
            self._name = str(args[0])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: description or name
        """
        if len(args) != 1:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0:
            raise ValueError("Empty name or description")
        return True

    @property
    def aggressorDb(self):
        """
        get the aggressor db object
        """
        return self._aggressorDb

    @aggressorDb.setter
    def aggressorDb(self, value):
        """
        set the aggressor db object
        """
        self._aggressorDb = value

    @property
    def idAggressor(self):
        """
        get the aggressor id
        """
        return self._idAggressor

    @property
    def name(self):
        """
        get the aggressor name or description
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        modify the aggressor name o description
        """
        self._name = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idAggressor"] = self._idAggressor
        new_dict["name"] = self._name

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all aggressor from db
        """
        data = cls.aggressorRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by aggressor key
        """
        return self.aggressorRefer.get()

    def write(self):
        """
        create a new aggresor in database
        return aggressor key
        """
        if (self.aggressorDb is None):
            self.aggressorDb = Aggressor.aggressorRefer.push(
                self.create_dict()
            )
            self._referDb = storage.db.reference(
                "{}/{}".format("aggressor", self.aggressorDb.key)
            )
            return self.aggressorDb.key
        else:
            return self.update()

    def update(self):
        """
        update the aggressor with new values
        return key aggressor
        """
        self.aggressorDb.update(self.create_dict())
        return self.aggressorDb.key

    def delete(self):
        """
        delete the aggressor
        """
        self.aggressorDb.delete()

    @classmethod
    def validAggressor(cls, idAggressor):
        """
        verify if a aggressor exists
        """
        for item in cls.readAll().values():
            if item.get('idAggressor') == idAggressor:
                return True
        return False
