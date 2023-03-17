import datetime
from typing import List

from gino import Gino
from sqlalchemy import Column, Integer, String, Text, Date

db = Gino()


class Client(db.Model):
    __tablename__ = 'clients'

    FIO = Column(Text, primary_key=True)
    gender = Column(String, nullable=True)
    age = Column(Date, nullable=True)
    mobile_phone = Column(Text, nullable=True)
    skin_type = Column(Text, nullable=True)
    chronic_diseases = Column(Text, nullable=True)
    medication = Column(Text, nullable=True)
    date_of_receipt = Column(Text, nullable=True)
    manipulations = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)