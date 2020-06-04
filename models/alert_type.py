#!/usr/bin/python3
"""
Alert class
"""
from models import storage
from uuid import uuid4
from datetime import datetime


class Alerttype:
    """
    """

    alerttypeRefer = storage.db.reference('alert_type')

    def __init__(self, *args, **kwargs):
        """
        args: create alert type object
            0: name or description alert type
        kwargs: create an object alert type with data from db
        """
        self._referDb = None
        self._alerttypeDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Alerttype.valid_args(args):
            self._idAlerttype = str(uuid4())
            self._name = str(args[0])
            self._level = int(args[1])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: description or name
        """
        if len(args) != 2:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0:
            raise ValueError("Empty name or description")
        if type(args[1]) != int:
            raise ValueError("Level need to be type int")
        return True

    @property
    def alerttypeDb(self):
        """
        get the alert object bd
        """
        return self._alerttypeDb

    @alerttypeDb.setter
    def alerttypeDb(self, value):
        """
        modify the alert bd object
        """
        self._alerttypeDb = value

    @property
    def idAlerttype(self):
        """
        get the alert type id
        """
        return self._idAlerttype

    @property
    def name(self):
        """
        get the alert type name or description
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        modify the alert type name or description
        """
        self._name = value

    @property
    def level(self):
        """
        get the alert type level
        """
        return self._level

    @level.setter
    def level(self, value):
        """
        modify the alert type level
        """
        self._level = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idAlerttype"] = self.idAlerttype
        new_dict["name"] = self.name
        new_dict["level"] = self.level

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all alert type from db
        """
        data = cls.alerttypeRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by alert type key
        """
        return self.alerttypeRefer.get()

    def write(self):
        """
        create a new alert type in database
        return key alert type
        """
        if (self.alerttypeDb is None):
            self.alerttypeDb = Alerttype.alerttypeRefer.push(
                self.create_dict()
            )
            self._referDb = storage.db.reference(
                "{}/{}".format("alert_type", self.alerttypeDb.key)
            )
            return self.alerttypeDb.key
        else:
            return self.update()

    def update(self):
        """
        update the alert type with new values
        return key alert type
        """
        self.alerttypeDb.update(self.create_dict())
        return self.alerttypeDb.key

    def delete(self):
        """
        delete the alert
        """
        self.alerttypeDb.delete()

    @classmethod
    def validAlerttype(cls, idAlerttype):
        """
        verify if a alert type exists
        """
        for item in cls.readAll().values():
            if item.get('idAlerttype') == idAlerttype:
                return True
        return False
