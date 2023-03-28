#!/usr/bin/python3
""" instances amenities """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.place import Place
from os import getenv

STORAGE = getenv("HBNB_TYPE_STORAGE")


class Amenity(BaseModel, Base):
    """Permit to add the amenities for places"""
    __tablename__ = "amenities"
    if STORAGE == "db":
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            'Place', secondary=Place.place_amenity)

    else:
        name = ""
