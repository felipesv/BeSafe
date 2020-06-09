#!/usr/bin/python3
""" 
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from public.config import ADDRESS_EMAIL, ADDRESS_PASS


class CheckEmail:
    """[summary]
    """
    def __init__(self, receiver_address):
        self.__sender_address = None
        self.__sender_pass = None
        self.__receiver = receiver_address

    @property
    def receiver(self):
        """ receiver getter

        Return: receiver
        """
        return self.__receiver

    @receiver.setter
    def receiver(self, value):
        """
        """
        self.__receiver = value

    
