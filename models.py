import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Train(Base):
    __tablename__ = 'training_data'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipe_id = Column(Integer)
    cuisine = Column(String(20))
    ingredients = relationship("Ingredients", backref="training_data")

    def __repr__(self):
        return "<Train(recipe_id='%d', cuisine='%s')>" % (self.recipe_id, self.cuisine)

class Ingredients(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    train_id = Column(Integer, ForeignKey("training_data.id"), primary_key=True)
    ingredient = Column(String(500))
