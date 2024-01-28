#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete", backref="state")
    else:
        name = ""

    @property
    def cities(self):
        """Returns the list of City instances with state_id equals
        to the current State.id"""
        from models import storage
        from models.city import City
        cities_list = []
        for key, value in storage.all(City).items():
            if value.state_id == self.id:
                cities_list.append(value)
        return cities_list

    def __init__(self, *args, **kwargs):
        """initializes State"""
        super().__init__(*args, **kwargs)
