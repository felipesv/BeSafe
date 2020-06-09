#!/usr/bin/python3
"""
Neighborhood class
"""
from models.comunas import Comunas
from models import storage
from uuid import uuid4


class Neighborhood:
    """
    """

    neighborhoodRefer = storage.db.reference('neighborhood')

    def __init__(self, *args, **kwargs):
        """
        args: create neighborhood class object
            0: comuna id
            1: neighborhood name or description
        kwargs: create a object neighborhood with data from db
        """
        self._referDb = None
        self._neighborhoodDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Neighborhood.valid_args(args):
            self._idNeighborhood = str(uuid4())
            self._idComuna = str(args[0])
            self._name = str(args[1])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: comuna id
            1: neighborhood name or description
        """
        if len(args) != 2:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0 or not Comunas.validComuna(args[0]):
            raise ValueError("Empty or not valid comuna id")
        if len(args[1]) == 0:
            raise ValueError("Empty name or descriprion")
        return True

    @property
    def neighborhoodDb(self):
        """
        get the neighborhood object db
        """
        return self._neighborhoodDb

    @neighborhoodDb.setter
    def neighborhoodDb(self, value):
        """
        set the neighborhood object db
        """
        self._neighborhoodDb = value

    @property
    def idNeighborhood(self):
        """
        get neighborhood id
        """
        return self._idNeighborhood

    @property
    def idComuna(self):
        """
        get comuna id
        """
        return self._idComuna

    @idComuna.setter
    def idComuna(self, value):
        """
        modify comuna id
        """
        self._idComuna = value

    @property
    def name(self):
        """
        get neighborhood name or description
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        modify neighborhood name or description
        """
        self._name = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idNeighborhood"] = self.idNeighborhood
        new_dict["idComuna"] = self._idComuna
        new_dict["name"] = self.name

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all neighborhood from db
        """
        data = cls.neighborhoodRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by neighborhood key
        """
        return self.neighborhoodRefer.get()

    def write(self):
        """
        create a new neighborhood in database
        return key neighborhood
        """
        if (self.neighborhoodDb is None):
            self.neighborhoodDb = Neighborhood.neighborhoodRefer.push(
                self.create_dict()
            )
            self._referDb = storage.db.reference(
                "{}/{}".format("neighborhood", self.neighborhoodDb.key)
            )
            return self.neighborhoodDb.key
        else:
            return self.update()

    def update(self):
        """
        update the neighborhood with new values
        return key neighborhood
        """
        self.neighborhoodDb.update(self.create_dict())
        return self.neighborhoodDb.key

    def delete(self):
        """
        delete the neighborhood
        """
        self.neighborhoodDb.delete()

    @classmethod
    def validNeighborhood(cls, idNeighborhood):
        """
        verify if a neighborhood exists
        """
        for item in cls.readAll().values():
            if item.get('idNeighborhood') == idNeighborhood:
                return True
        return False
