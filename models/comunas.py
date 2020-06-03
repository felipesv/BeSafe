#!/usr/bin/python3
"""
Comunas class
"""
from models import storage
from uuid import uuid4


class Comunas:
    """
    """

    comunaRefer = storage.db.reference('comunas')

    def __init__(self, *args, **kwargs):
        """
        args: create comuna class object
            0: comuna name or description
        kwargs: create a object comuna with data from db
        """
        self._referDb = None
        self._comunaDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Comunas.valid_args(args):
            self._idComuna = str(uuid4())
            self._name = str(args[0])
            self._color = str(args[1])
            self._openstreetcod = str(args[2])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: comuna name or description
        """
        if len(args) != 3:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0:
            raise ValueError("Empty name or descriprion")
        if len(args[1]) == 0:
            raise ValueError("Empty name or descriprion")
        if len(args[2]) == 0:
            raise ValueError("Empty name or descriprion")
        return True

    @property
    def comunaDb(self):
        """
        get the comuna object db
        """
        return self._comunaDb

    @comunaDb.setter
    def comunaDb(self, value):
        """
        set the comuna object db
        """
        self._comunaDb = value

    @property
    def idComuna(self):
        """
        get comuna id
        """
        return self._idComuna

    @property
    def name(self):
        """
        get comuna name or description
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        modify comuna name or description
        """
        self._name = value

    @property
    def color(self):
        """
        get comuna color or description
        """
        return self._color

    @color.setter
    def color(self, value):
        """
        modify comuna color or description
        """
        self._color = value

    @property
    def openstreetcod(self):
        """
        get comuna openstreetcod or description
        """
        return self._openstreetcod

    @openstreetcod.setter
    def openstreetcod(self, value):
        """
        modify comuna openstreetcod or description
        """
        self._openstreetcod = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idComuna"] = self.idComuna
        new_dict["name"] = self.name
        new_dict["color"] = self.color
        new_dict["openstreetcod"] = self.openstreetcod

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all comuna from db
        """
        data = cls.comunaRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by comuna key
        """
        return self.comunaRefer.get()

    def write(self):
        """
        create a new comuna in database
        return key comuna
        """
        if (self.comunaDb is None):
            self.comunaDb = Comunas.comunaRefer.push(
                self.create_dict()
            )
            self._referDb = storage.db.reference(
                "{}/{}".format("comunas", self.comunaDb.key)
            )
            return self.comunaDb.key
        else:
            return self.update()

    def update(self):
        """
        update the comuna with new values
        return key comuna
        """
        self.comunaDb.update(self.create_dict())
        return self.comunaDb.key

    def delete(self):
        """
        delete the comuna
        """
        self.comunaDb.delete()

    @classmethod
    def validComuna(cls, idComuna):
        """
        verify if a comuna exists
        """
        for item in cls.readAll().values():
            if item.get('idComuna') == idComuna:
                return True
        return False

    def addCoordinate(self, dictCoor):
        """
        """
        path = "comunas/{}/coordinates".format(self.comunaDb.key)
        coordRefer = storage.db.reference(path)
        for key, val in dictCoor.items():
            coordRefer.push({key: val})
