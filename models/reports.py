#!/usr/bin/python3
"""
Reports class
"""
from models import storage
from models.alerts import Alert
from models.aggressor import Aggressor
from models.collective_group import Collectivegroup
from models.neighborhood import Neighborhood
from models.stage import Stage
from uuid import uuid4
from datetime import datetime


class Reports:
    """
    """

    reportRefer = storage.db.reference('reports')

    def __init__(self, *args, **kwargs):
        """
        args: create a new role type object
            0: alert id
            1: report description
            2: neighborhood id
            3: stage id
            4: aggressor id
            5: complaint
            6: collective group id
        kwargs: create a object role type with data from db
        """
        self._referDb = None
        self._reportDb = None
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        elif Reports.valid_args(args):
            self._idReport = str(uuid4())
            self._idAlert = str(args[0])
            self._description = str(args[1])
            self._idNeighborhood = str(args[2])
            self._idStage = str(args[3])
            self._date = datetime.now().strftime("%m/%d/%Y")
            self._hour = datetime.now().strftime("%H:%M:%S")
            self._idAggressor = str(args[4])
            self._complaint = str(args[5])
            self._idCollective = str(args[6])

    @classmethod
    def valid_args(cls, args):
        """
        verify if all the values are correct
            0: alert id
            1: report description
            2: neighborhood id
            3: stage id
            4: aggressor id
            5: complaint
            6: collective group id
        """
        if len(args) != 7:
            raise SyntaxError("Incorrect number of attributes")
        if len(args[0]) == 0 or not Alert.validAlert(args[0]):
            raise ValueError("Empty or not a valid alert id")
        if len(args[1]) == 0:
            raise ValueError("Empty report description")
        if len(args[2]) == 0 or not Neighborhood.validNeighborhood(args[2]):
            raise ValueError("Empty or not a valid neighborhood id")
        if len(args[3]) == 0 or not Stage.validStage(args[3]):
            raise ValueError("Empty or not a valid stage id")
        if len(args[4]) == 0 or not Aggressor.validAggressor(args[4]):
            raise ValueError("Empty or not a valid aggressor id")
        if len(args[5]) == 0:
            raise ValueError("Empty complaint")
        if len(args[6]) == 0 or not Collectivegroup.validCollective(args[6]):
            raise ValueError("Empty or not a valid collective group id")
        return True

    @property
    def reportDb(self):
        """
        get the report object db
        """
        return self._reportDb

    @reportDb.setter
    def reportDb(self, value):
        """
        modify the report object db
        """
        self._reportDb = value

    @property
    def idReport(self):
        """
        get the report id
        """
        return self._idReport

    @property
    def idAlert(self):
        """
        get the alert id
        """
        return self._idAlert

    @idAlert.setter
    def idAlert(self, value):
        """
        modify the alert id
        """
        self._idAlert = value

    @property
    def description(self):
        """
        get the report description
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        modify the report description
        """
        self._description = value

    @property
    def idNeighborhood(self):
        """
        get the neighborhood id
        """
        return self._idNeighborhood

    @idNeighborhood.setter
    def idNeighborhood(self, value):
        """
        modify the neighborhood id
        """
        self._idNeighborhood = value

    @property
    def idStage(self):
        """
        get the stage id
        """
        return self._idStage

    @idStage.setter
    def idStage(self, value):
        """
        modify the stage id
        """
        self._idStage = value

    @property
    def date(self):
        return self._date

    @property
    def hour(self):
        return self._hour

    @property
    def idAggressor(self):
        """
        get the id aggressor
        """
        return self._idAggressor

    @idAggressor.setter
    def idAggressor(self, value):
        """
        modify the id aggressor
        """
        self._idAggressor = value

    @property
    def complaint(self):
        """
        get the report complaint
        """
        return self._complaint

    @complaint.setter
    def complaint(self, value):
        """
        modify the report complaint
        """
        self._complaint = value

    @property
    def idCollective(self):
        """
        get the collective group id
        """
        return self._idCollective

    @idCollective.setter
    def idCollective(self, value):
        """
        get the collective group id
        """
        self._idCollective = value

    def create_dict(self):
        """
        create dict to save in db
        """
        new_dict = {}
        new_dict['idReport'] = self.idReport
        new_dict['idAlert'] = self.idAlert
        new_dict['description'] = self.description
        new_dict['idNeighborhood'] = self.idNeighborhood
        new_dict['idStage'] = self.idStage
        new_dict['date'] = self.date
        new_dict['hour'] = self.hour
        new_dict['idAggressor'] = self.idAggressor
        new_dict['complaint'] = self.complaint
        new_dict['idCollective'] = self.idCollective

        return new_dict

    @classmethod
    def readAll(cls):
        """
        get all reports from db
        """
        data = cls.reportRefer.get()
        if data is None:
            return {}
        return data

    def read(self):
        """
        get all the information from db by reports key
        """
        return self.reportRefer.get()

    def write(self):
        """
        create a new reports in database
        return key reports
        """
        if (self.reportDb is None):
            self.reportDb = Reports.reportRefer.push(self.create_dict())
            self._referDb = storage.db.reference("{}/{}".format(
                "reports", self.reportDb.key)
            )
            return self.reportDb.key
        else:
            return self.update()

    def update(self):
        """
        update the reports with new values
        return key reports
        """
        self.reportDb.update(self.create_dict())
        return self.reportDb.key

    def delete(self):
        """
        delete the report
        """
        self.reportDb.delete()

    @classmethod
    def validReport(cls, idReport):
        """
        verify if a report exists
        """
        for item in cls.readAll().values():
            if item.get('idReport') == idReport:
                return True
        return False
