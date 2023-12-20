#!/usr/bin/python3
""" DbStorage Module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """ Init method """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ All method """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            objs = self.__session.query(cls).all()
        return {"{}.{}".format(type(obj).__name__, obj.id): obj
                for obj in objs}

    def new(self, obj):
        """ New method """
        self.__session.add(obj)

    def save(self):
        """ Save method """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete method """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Reload method """
        Base.metadata.create_all(self.__engine)
        sf = sessionmaker(bind=self.__engine,
                          expire_on_commit=False)
        Session = scoped_session(sf)
        self.__session = Session()

    def close(self):
        """ Close method """
        self.__session.close()
