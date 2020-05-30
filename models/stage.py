#!/usr/bin/python3
"""
Stage class
"""
from models import storage
from uuid import uuid4


class Stage:
    """
    """

    stageRefer = storage.db.reference('stages')

    def __init__(self, *args, **kwargs):
        """
        args: create stages object
            0: stage name or description
        kwargs: create a object stages with data from db
        """
        self._referDb = None
        self._stagesDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Stage.valid_args(args):
            self._idStage = str(uuid4())
            self._name = str(args[0])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: neighborhood name or description
        """
        if len(args) != 1:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0:
            raise ValueError("Empty name or descriprion")
        return True

    @property
    def stagesDb(self):
        """
        get stage object db
        """
        return self._stagesDb

    @stagesDb.setter
    def stagesDb(self, value):
        """
        modify stageobject db
        """
        self._stagesDb = value

    @property
    def idStage(self):
        """
        get the stage id
        """
        return self._idStage

    @property
    def name(self):
        """
        get the stage name or description
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        modify the stage name or description
        """
        self._name = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict["idStages"] = self.idStage
        new_dict["name"] = self.name

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all stages from db
        """
        data = cls.stageRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by stages key
        """
        return self.stageRefer.get()

    def write(self):
        """
        create a new stage in database
        return key stage
        """
        if (self.stagesDb is None):
            self.stagesDb = Stage.stageRefer.push(self.create_dict())
            self._referDb = storage.db.reference(
                "{}/{}".format("stages", self.stagesDb.key)
            )
            return self.stagesDb.key
        else:
            return self.update()

    def update(self):
        """
        update the stages with new values
        return key stages
        """
        self.stagesDb.update(self.create_dict())
        return self.stagesDb.key

    def delete(self):
        """
        delete the stage
        """
        self.stagesDb.delete()

    @classmethod
    def validStage(cls, idStages):
        """
        verify if a stage exists
        """
        for item in cls.readAll().values():
            if item.get('idStages') == idStages:
                return True
        return False
