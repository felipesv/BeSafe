#!/usr/bin/python3
"""
Notification class
"""
from models import storage
from uuid import uuid4
from datetime import datetime


class Notification:
    """
    """

    notificationRefer = storage.db.reference('notification')

    def __init__(self, *args, **kwargs):
        """
        args: create notification object
            0: notification message
        kwargs: create a object notification with data from db
        """
        self._referDb = None
        self._notificationDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Notification.valid_args(args):
            self._idNotification = str(uuid4())
            self._date = datetime.now().strftime("%m/%d/%Y")
            self._hour = datetime.now().strftime("%H:%M:%S")
            self._message = str(args[0])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: notification message
        """
        if len(args) != 1:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0:
            raise ValueError("Empty message")
        return True

    @property
    def notificationDb(self):
        """
        get notification object db
        """
        return self._notificationDb

    @notificationDb.setter
    def notificationDb(self, value):
        """
        modify notification object db
        """
        self._notificationDb = value

    @property
    def idNotification(self):
        """
        get the notification id
        """
        return self._idNotification

    @property
    def date(self):
        """
        get the date
        """
        return self._date

    @property
    def hour(self):
        """
        get the hour
        """
        return self._hour

    @property
    def message(self):
        """
        get the notification message
        """
        return self._message

    @message.setter
    def message(self, value):
        """
        modify the notification message
        """
        self.message = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idNotification"] = self.idNotification
        new_dict["date"] = self.date
        new_dict["hour"] = self.hour
        new_dict["message"] = self.message

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all notification from db
        """
        data = cls.notificationRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the notifcation from db by alert key
        """
        return self.notificationRefer.get()

    def write(self):
        """
        create a new notification in database
        return notification alert
        """
        if (self.notificationDb is None):
            self.notificationDb = Notification.notificationRefer.push(
                self.create_dict()
            )
            self._referDb = storage.db.reference(
                "{}/{}".format("notification", self.notificationDb.key)
            )
            return self.notificationDb.key
        else:
            return self.update()

    def update(self):
        """
        update the notification with new values
        return key notification
        """
        self.notificationDb.update(self.create_dict())
        return self.notificationDb.key

    def delete(self):
        """
        delete the notification
        """
        self.notificationDb.delete()

    @classmethod
    def validNotification(cls, idNotification):
        """
        verify if a notification exists
        """
        for item in cls.readAll().values():
            if item.get('idNotification') == idNotification:
                return True
        return False
