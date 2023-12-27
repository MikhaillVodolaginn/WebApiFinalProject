from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    cities = relationship('City', back_populates='country')
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship('Country', back_populates='cities')
    streets = relationship('Street', back_populates='city')
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())


class Street(Base):
    __tablename__ = 'streets'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship('City', back_populates='streets')
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
