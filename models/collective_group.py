#!/usr/bin/python3
"""
Collective group class
"""
from models import storage
from uuid import uuid4


class Collectivegroup:
    """
    """

    collectiveRefer = storage.db.reference('collective_group')

    def __init__(self, *args, **kwargs):
        """
        args: create collective type object
            0: collective group name or description
        kwargs: create a object collective with data from db
        """
        self._referDb = None
        self._collectiveDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Collectivegroup.valid_args(args):
            self._idCollective = str(uuid4())
            self._name = str(args[0])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: collective group name or description
        """
        if len(args) != 1:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0:
            raise ValueError("Empty name or description")
        return True

    @property
    def collectiveDb(self):
        """
        get the collective object db
        """
        return self._collectiveDb

    @collectiveDb.setter
    def collectiveDb(self, value):
        """
        modify the collective object db
        """
        self._collectiveDb = value

    @property
    def idCollective(self):
        """
        get the collective group id
        """
        return self._idCollective

    @property
    def name(self):
        """
        get the collective group name or description
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        modify the collective group name or description
        """
        self._name = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idCollective"] = self.idCollective
        new_dict["name"] = self.name

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all collective group from db
        """
        data = cls.collectiveRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by collective group key
        """
        return self.collectiveRefer.get()

    def write(self):
        """
        create a new collective group in database
        return key collective group
        """
        if (self.collectiveDb is None):
            self.collectiveDb = Collectivegroup.collectiveRefer.push(
                self.create_dict()
            )
            self._referDb = storage.db.reference(
                "{}/{}".format("collective_group", self.collectiveDb.key)
            )
            return self.collectiveDb.key
        else:
            return self.update()

    def update(self):
        """
        update the collective group with new values
        return key collective group
        """
        self.collectiveDb.update(self.create_dict())
        return self.collectiveDb.key

    def delete(self):
        """
        delete the collective group
        """
        self.collectiveDb.delete()

    @classmethod
    def validCollective(cls, idCollective):
        """
        verify if a collective group exists
        """
        for item in cls.readAll().values():
            if item.get('idCollective') == idCollective:
                return True
        return False
