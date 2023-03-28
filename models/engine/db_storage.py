#!/usr/bin/python3
"""Db engine to store in the database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
import sqlalchemy
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """this class is the engine to store
    mysql database
    """
    __engine = None
    __session = None

    def __init__(self):
        """initialization
        """
        USER = getenv('HBNB_MYSQL_USER')
        PASSWORD = getenv('HBNB_MYSQL_PWD')
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')
        ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            USER,
            PASSWORD,
            HOST,
            DB), pool_pre_ping=True)
        if ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """show the requested data from database"""
        show = {}
        classes = {
            'State': State, 'City': City,
            'Amenity': Amenity, 'User': User,
            'Place': Place, 'Review': Review}

        if cls is not None:
            objects = self.__session.query(cls).all()
            for obj in objects:
                show[obj.to_dict()['__class__'] + '.' + obj.id] = obj
        else:
            for clase, value in classes.items():
                objects = self.__session.query(value).all()
                for obj in objects:
                    show[obj.to_dict()['__class__'] + '.' + obj.id] = obj
        return show

    def new(self, obj):
        """add data to db"""
        self.__session.add(obj)

    def save(self):
        """store the added data"""
        self.__session.commit()

    def delete(self, obj=None):
        """remove data"""
        self.__session.detele(obj)

    def reload(self):
        """create all reload data
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(
            session_factory)

    def close(self):
        """call remove() method on the private session attribute
        (self.__session) tips or close() on the class Session"""
        self.__session.remove()
