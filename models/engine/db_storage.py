#!/usr/bin/python3

"""db_storage"""

from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DBStorage:
    __engine = None
    __session = None
    __dict_classes = {
        "State": State,
        "City": City,
        "User": User,
        "Place": Place,
        "Review": Review,
        "Amenity": Amenity}

    def __init__(self):
        """Constructor for DBStorage"""
        username = os.getenv('HBNB_MYSQL_USER')
        psw = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(username, psw, host, db_name),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Retrieve all objects from database"""
        _dict = {}
        if cls is None:
            for key, cls in self.__dict_classes.items():
                for obj in self.__session.query(cls):
                    _dict["{}.{}".format(cls.__name__, obj.id)] = obj
        else:
            for obj in self.__session.query(self.__dict_classes.get(cls)):
                _dict["{}.{}".format(
                    self.__dict_classes.get(cls).__name__, obj.id)] = obj
        return _dict

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        """call remove method on the private session"""
        self.__session.close()
