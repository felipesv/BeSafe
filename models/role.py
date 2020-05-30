#!/usr/bin/python3
"""
Role class
"""
from models import storage
from uuid import uuid4


class Role:
    """
    """

    roleRefer = storage.db.reference('role_types')

    def __init__(self, *args, **kwargs):
        """
        args: create a new role type object
            0: rol name or description
        kwargs: create a object role type with data from db
        """
        self._referDb = None
        self._roleDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Role.valid_args(args):
            self._idRol = str(uuid4())
            self._description = str(args[0])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: rol name or description
        """
        if len(args) != 1:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0:
            raise ValueError("Empty name or description")
        return True

    @property
    def roleDb(self):
        """
        get the rol object db
        """
        return self._roleDb

    @roleDb.setter
    def roleDb(self, value):
        """
        modify the rol object db
        """
        self._roleDb = value

    @property
    def idRol(self):
        """
        get the rol id
        """
        return self._idRol

    @property
    def description(self):
        """
        get the rol name or description
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        modify the rol name or description
        """
        self._description = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idRol"] = self.idRol
        new_dict["description"] = self.description

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all roles from db
        """
        data = cls.roleRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by role key
        """
        return self.roleDb.get()

    def write(self):
        """
        create a new role in database
        return key role
        """
        if (self.roleDb is None):
            self.roleDb = Role.roleRefer.push(self.create_dict())
            self._referDb = storage.db.reference(
                "{}/{}".format("role_types", self.roleDb.key)
            )
            return self.roleDb.key
        else:
            return self.update()

    def update(self):
        """
        update the role with new values
        return key role
        """
        self.roleDb.update(self.create_dict())
        return self.roleDb.key

    def delete(self):
        """
        delete the role
        """
        self.roleDb.delete()

    @classmethod
    def validRole(cls, idRol):
        """
        verify if a role exists
        """
        for item in cls.readAll().values():
            if item.get('idRol') == idRol:
                return True
        return False
