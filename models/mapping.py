#!/usr/bin/python3
"""
Mapping class
"""
from models import storage
from models.reports import Reports
from uuid import uuid4


class Mapping:
    """
    """

    mappingRefer = storage.db.reference('mapping')

    def __init__(self, *args, **kwargs):
        """
        args: create mapping type object
            0: report id
            1: latitude
            2: longitude
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
            self._latitude = float(args[1])
            self._longitude = float(args[2])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: report id
            1: latitude
            2: longitude
        """
        if len(args) != 3:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0 or not Reports.validReport(args[0]):
            raise ValueError("Empty or not a valid report id")
        if type(args[1]) is not float:
            raise ValueError("Latitude needs to be a float data type")
        if type(args[2]) is not float:
            raise ValueError("Longitude needs to be a float data type")
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
        return self._latitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idMapping"] = self.idMapping
        new_dict["idReport"] = self.idReport
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
