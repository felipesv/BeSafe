#!/usr/bin/python3
"""
User Class
"""
from models import storage
from models.role import Role
from uuid import uuid4


class User:
    """
    """

    userRefer = storage.db.reference('users')

    def __init__(self, *args, **kwargs):
        """
        args: create a new user object
            0: rol id
            1: user name
            2: user email
            3: user password
        kwargs: create a object user with data from db
        """
        self._referDb = None
        self._userDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif User.valid_args(args):
            self._idUser = str(uuid4())
            self._idRol = str(args[0])
            self._name = str(args[1])
            self._email = str(args[2])
            self._password = str(args[3])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: rol id
            1: user name
            2: user email
            3: user password
        """
        if len(args) != 4:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0 or not Role.validRole(args[0]):
            raise ValueError("Empty or not a valid report id")
        if len(args[1]) == 0:
            raise ValueError("Empty name")
        if len(args[2]) == 0 or User.validUser(args[2]):
            raise ValueError("Empty or email exist")
        if len(args[3]) == 0:
            raise ValueError("Empty password")
        return True

    @property
    def userDb(self):
        """
        get the user object db
        """
        return self._userDb

    @userDb.setter
    def userDb(self, value):
        """
        modify the user object db
        """
        self._userDb = value

    @property
    def idUser(self):
        """
        get the user id
        """
        return self._idUser

    @property
    def idRol(self):
        """
        get the rol id
        """
        return self._idRol

    @idRol.setter
    def idRol(self, value):
        """
        modify the rol id
        """
        self._idRol = value

    @property
    def name(self):
        """
        get the user name
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        modify the user name
        """
        self._name = value

    @property
    def email(self):
        """
        get the user email
        """
        return self._email

    @email.setter
    def email(self, value):
        """
        modify the user email
        """
        self._email = value

    @property
    def password(self):
        """
        get the usee password
        """
        return self._password

    @password.setter
    def password(self, value):
        """
        modify the user password
        """
        self._password = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idUser"] = self.idUser
        new_dict["idRol"] = self.idRol
        new_dict["name"] = self.name
        new_dict["email"] = self.email
        new_dict["password"] = self.password

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all users from db
        """
        data = cls.userRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by user key
        """
        return self.userDb.get()

    def write(self):
        """
        create a new user in database
        return key
        """
        if (self.userDb is None):
            self.userDb = User.userRefer.push(self.create_dict())
            self._referDb = storage.db.reference(
                "{}/{}".format("users", self.userDb.key)
            )
            return self.userDb.key
        else:
            return self.update()

    def update(self):
        """
        update the user with new values
        return key
        """
        self.userDb.update(self.create_dict())
        return self.userDb.key

    def delete(self):
        """
        delete the user
        """
        self.userDb.delete()

    @classmethod
    def validUser(cls, email):
        """
        verify if a user exists
        """
        for item in cls.readAll().values():
            if item.get('email') == email:
                return True
        return False

    @classmethod
    def validUserId(cls, idUser):
        """
        verify if a user exists by id
        """
        for item in cls.readAll().values():
            if item.get('idUser') == idUser:
                return True
        return False
