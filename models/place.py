#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review", backref="place",
                               cascade="all, delete")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """ Getter for reviews """
            from models import storage
            from models.review import Review
            rList = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    rList.append(review)
            return rList

        @property
        def amenities(self):
            """ Getter for amenities """
            from models import storage
            from models.amenity import Amenity
            aList = []
            for amenity in storage.all(Amenity).values():
                if amenity.place_id == self.id:
                    aList.append(amenity)
            return aList

        @amenities.setter
        def amenities(self, obj):
            """ Setter for amenities """
            from models.amenity import Amenity
            if type(obj) is Amenity:
                self.amenity_ids.append(obj.id)
