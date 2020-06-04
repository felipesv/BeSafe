#!/usr/bin/python3
"""
Mapping class
"""
from models import storage
from models.reports import Reports
from models.alert_type import Alerttype
from models.user import User
from uuid import uuid4


class Mapping:
    """
    """

    mappingRefer = storage.db.reference('mapping')

    def __init__(self, *args, **kwargs):
        """
        args: create mapping type object
            0: report id
            1: alert type id
            2: latitude
            3: longitude
            4: user id
        kwargs: create a object mapping with data from db
        """
        self._referDb = None
        self._mappingDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Mapping.valid_args(args):
            self._idMapping = str(uuid4())
            self._idReport = str(args[0])
            self._idAlerttype = str(args[1])
            self._latitude = float(args[2])
            self._longitude = float(args[3])
            self._idUser = str(args[4])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: report id
            1: alert type id
            2: latitude
            3: longitude
            4: user id
        """
        if len(args) != 5:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0 or not Reports.validReport(args[0]):
            raise ValueError("Empty or not a valid report id")
        if len(args[1]) == 0 or not Alerttype.validAlerttype(args[1]):
            raise ValueError("Empty or not a valid alert type id")
        if type(args[2]) is not float:
            raise ValueError("Latitude needs to be a float data type")
        if type(args[3]) is not float:
            raise ValueError("Longitude needs to be a float data type")
        if len(args[4]) == 0 or not User.validUserId(args[4]):
            raise ValueError("Empty or not a valid user id")
        return True

    @property
    def mappingDb(self):
        """
        get the mapping object db
        """
        return self._mappingDb

    @mappingDb.setter
    def mappingDb(self, value):
        """
        modify the mapping object db
        """
        self._mappingDb = value

    @property
    def idMapping(self):
        """
        get the mapping id
        """
        return self._idMapping

    @property
    def idReport(self):
        """
        get the report id
        """
        return self._idReport

    @idReport.setter
    def idReport(self, value):
        """
        modify the report id
        """
        self._idReport = value

    @property
    def idAlerttype(self):
        """
        get alert type id
        """
        return self._idAlerttype

    @idAlerttype.setter
    def idAlerttype(self, value):
        """
        modify alert type id
        """
        self._idAlerttype = value

    @property
    def latitude(self):
        """
        get the mapping latitude
        """
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """
        modify the mapping latitude
        """
        self._latitude = value

    @property
    def longitude(self):
        """
        get the mapping longitude
        """
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """
        modify the mapping longitude
        """
        self._longitude = value

    @property
    def idUser(self):
        """
        get the mapping longitude
        """
        return self._idUser

    @idUser.setter
    def idUser(self, value):
        """
        modify the user id
        """
        self._idUser = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idMapping"] = self.idMapping
        new_dict["idReport"] = self.idReport
        new_dict["idAlerttype"] = self.idAlerttype
        new_dict["latitude"] = self.latitude
        new_dict["longitude"] = self.longitude

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all mapping from db
        """
        data = cls.mappingRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by mapping key
        """
        return self.mappingRefer.get()

    def write(self):
        """
        create a new mapping in database
        return key mapping
        """
        if (self.mappingDb is None):
            self.mappingDb = Mapping.mappingRefer.push(self.create_dict())
            self._referDb = storage.db.reference(
                "{}/{}".format("mapping", self.mappingDb.key)
            )
            return self.mappingDb.key
        else:
            return self.update()

    def update(self):
        """
        update the mapping with new values
        return key mapping
        """
        self.mappingDb.update(self.create_dict())
        return self.mappingDb.key

    def delete(self):
        """
        delete the mapping
        """
        self.mappingDb.delete()

    @classmethod
    def validMapping(cls, idMapping):
        """
        verify if a mapping exists
        """
        for item in cls.readAll().values():
            if item.get('idMapping') == idMapping:
                return True
        return False
