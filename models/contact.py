#!/usr/bin/python3
"""
Contact Class
"""
from models import storage
from models.role import Role
from uuid import uuid4


class Contact:
    """
    """

    contactRefer = storage.db.reference('contact')

    def __init__(self, *args, **kwargs):
        """
        args: create a new user object
            0: name
            1: city
            2: email
            3: message
        kwargs: create a object contact with data from db
        """
        self._referDb = None
        self._contactDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Contact.valid_args(args):
            self._idContact = str(uuid4())
            self._name = str(args[0])
            self._city = str(args[1])
            self._email = str(args[2])
            self._message = str(args[3])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: name
            1: city
            2: email
            3: message
        """
        if len(args) != 4:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0:
            raise ValueError("Empty or not a valid name")
        if len(args[1]) == 0:
            raise ValueError("Empty or not a valid city")
        if len(args[2]) == 0:
            raise ValueError("Empty or not a valid email")
        if len(args[3]) == 0:
            raise ValueError("Empty or not a valid message")
        return True

    @property
    def contactDb(self):
        """
        get the contact object db
        """
        return self._contactDb

    @contactDb.setter
    def contactDb(self, value):
        """
        modify the contact object db
        """
        self._contactDb = value

    @property
    def idContact(self):
        """
        get the contact id
        """
        return self._idContact

    @property
    def name(self):
        """
        get the name
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        modify the name
        """
        self._name = value

    @property
    def city(self):
        """
        get the city
        """
        return self._city

    @city.setter
    def city(self, value):
        """
        modify the city
        """
        self._city = value

    @property
    def email(self):
        """
        get the email
        """
        return self._email

    @email.setter
    def email(self, value):
        """
        modify the email
        """
        self._email = value

    @property
    def message(self):
        """
        get the message
        """
        return self._message

    @message.setter
    def message(self, value):
        """
        modify the message
        """
        self._message = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idContact"] = self.idContact
        new_dict["name"] = self.name
        new_dict["city"] = self.city
        new_dict["email"] = self.email
        new_dict["message"] = self.message

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all contact from db
        """
        data = cls.contactRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by contact key
        """
        return self.contactRefer.get()

    def write(self):
        """
        create a new contact in database
        return key contact
        """
        if (self.contactDb is None):
            self.contactDb = Contact.contactRefer.push(self.create_dict())
            self._referDb = storage.db.reference(
                "{}/{}".format("contact", self.contactDb.key)
            )
            return self.contactDb.key
        else:
            return self.update()

    def update(self):
        """
        update the contact with new values
        return key contact
        """
        self.contactDb.update(self.create_dict())
        return self.contactDb.key

    def delete(self):
        """
        delete the contact
        """
        self.contactDb.delete()
