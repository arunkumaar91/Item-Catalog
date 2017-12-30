import os
import sys
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()

#### DATABASE TABLES ####

# class definition for User


class User(Base):
  # table
  __tablename__ = 'user'
  # attributes
  id = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)
  email = Column(String(250), nullable=False)
  picture = Column(String(250))

# Ser Function to send JSON objects in serializeable format


@property
def serialize(self):
    """Return object data in easily serializable format"""
    return {
    'name': self.name,
    'id': self.id,
    }


# class definition for Category
class Category(Base):
  # table
  __tablename__ = 'category'
  # attributes
  name = Column(String(250), nullable=False)
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship(User)

# Ser Function to send JSON objects in serializeable format
@property
def serialize(self):
    """Return object data in serializable format"""
    return {
    'name': self.name,
    'id': self.id,
    }


# class definition for ListItems
class ListItems(Base):
  # table
  __tablename__ = 'list_item'
  # attributes
  name =Column(String(100), nullable = False)
  id = Column(Integer, primary_key = True)
  subcategory = Column(String(150))
  description = Column(String(700))
  price = Column(String(8))
  category_id = Column(Integer,ForeignKey(Category.id))
  category = relationship(Category)
  user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship(User)

# Ser Function to send JSON objects in serializeable format
@property
def serialize(self):
    """Return object data in easily serializable format"""
    return {
    'name': self.name,
    'description': self.description,
    'id': self.id,
    'price': self.price,
    'subcategory': self.subcategory,
    }


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)
