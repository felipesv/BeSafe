#!/usr/bin/python3
"""
Alert class
"""
from models import storage
from models.notification import Notification
from uuid import uuid4
from datetime import datetime


class Alert:
    """
    """

    alertRefer = storage.db.reference('alerts')

    def __init__(self, *args, **kwargs):
        """
        args: create alert object
            0: alert type id
            1: notification id
        kwargs: create an object alert with data from db
        """
        self._referDb = None
        self._alertDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Alert.valid_args(args):
            self._idAlert = str(uuid4())
            self._message = str(args[0])
            self._date = datetime.now().strftime("%m/%d/%Y")
            self._hour = datetime.now().strftime("%H:%M:%S")
            self._idNotification = str(args[1])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: alert type id
            1: notification id
        """
        if len(args) != 2:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0:
            raise ValueError("Empty name or description")
        if len(args[1]) == 0 or not Notification.validNotification(args[1]):
            raise ValueError("Empty or not a valid notification id")
        return True

    @property
    def alertDb(self):
        """
        get the alert object db
        """
        return self._alertDb

    @alertDb.setter
    def alertDb(self, value):
        """
        modify the alert object db
        """
        self._alertDb = value

    @property
    def idAlert(self):
        """
        get alert id
        """
        return self._idAlert

    @property
    def message(self):
        """
        get the alert message
        """
        return self._message

    @message.setter
    def message(self, value):
        """
        modify the alert message
        """
        self._message = value

    @property
    def date(self):
        """
        get the alert date
        """
        return self._date

    @property
    def hour(self):
        """
        get the alert hour
        """
        return self._hour

    @property
    def idNotification(self):
        """
        get notification id
        """
        return self._idNotification

    @idNotification.setter
    def idNotification(self, value):
        """
        modify notification id
        """
        self._idNotification = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idAlert"] = self.idAlert
        new_dict["message"] = self.message
        new_dict["date"] = self.date
        new_dict["hour"] = self.hour
        new_dict["idNotification"] = self.idNotification

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all alert from db
        """
        data = cls.alertRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by alert key
        """
        return self.alertRefer.get()

    def write(self):
        """
        create a new alert in database
        return key alert
        """
        if (self.alertDb is None):
            self.alertDb = Alert.alertRefer.push(self.create_dict())
            self._referDb = storage.db.reference(
                "{}/{}".format("alerts", self.alertDb.key)
            )
            return self.alertDb.key
        else:
            return self.update()

    def update(self):
        """
        update the alert with new values
        return key alert
        """
        self.alertDb.update(self.create_dict())
        return self.alertDb.key

    def delete(self):
        """
        delete the alert
        """
        self.alertDb.delete()

    @classmethod
    def validAlert(cls, idAlert):
        """
        verify if a alert exists
        """
        for item in cls.readAll().values():
            if item.get('idAlert') == idAlert:
                return True
        return False
