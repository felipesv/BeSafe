#!/usr/bin/python3
""" storages
"""

from models.database.firebase_db import Firebase_db
storage = Firebase_db()
storage.connect()
