import os, sys, logging
import sqlalchemy
import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import database_exists, create_database


LEVELS = { 'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL,
            }

if len(sys.argv) > 1:
    level_name = sys.argv[1]
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)

database_uri='postgresql://{0}:{1}@localhost/{2}'.format(sys.argv[1], sys.argv[2], sys.argv[3])

#check if database exists and if not create database convo
if not database_exists(database_uri):
    print 'Database {0} does not exist'.format(sys.argv[3])
    print 'Creating database {0}'.format(sys.argv[3])
    create_database(database_uri)
    print 'Database {0} created'.format(sys.argv[3])

#connect to sqlalchemy engine
engine = create_engine(database_uri)
Session = sessionmaker(bind=engine)
session=Session()

Base = declarative_base()

class Train(Base):
    __tablename__ = 'training_data'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipe_id = Column(Integer)
    cuisine = Column(String(20))
    ingredients = relationship("Ingredients", backref="training_data")

    def __repr__(self):
        return "<Train(recipe_id='%d', cuisine='%s')>" % (self.recipe_id, self.cuisine)

class Test(Base):
    __tablename__ = 'test_data'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipe_id = Column(Integer)
    ingredients = relationship("Test_Ingredients", backref="test_data")

    def __repr__(self):
        return "<Test(recipe_id='%d')>" % (self.recipe_id)

#create tables Node and node_to_node
Base.metadata.create_all(engine, checkfirst=True)

class Ingredients(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    train_id = Column(Integer, ForeignKey("training_data.id"), primary_key=True)
    ingredient = Column(String(500))

class Test_Ingredients(Base):
    __tablename__ = 'test_ingredients'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    test_id = Column(Integer, ForeignKey("test_data.id"), primary_key=True)
    ingredient = Column(String(500))

#create tables Node and node_to_node
Base.metadata.create_all(engine, checkfirst=True)




engine = create_engine('postgresql://train:kaggle@localhost/{0}'.format(sys.argv[3]))
Session = sessionmaker(bind=engine)
session=Session()


f=open('train.json', 'rb')
lines=''.join(f.readlines())
jlines = json.loads(lines)

for j in jlines:
  #add recipe
  new_recipe = Train(recipe_id=j['id'], cuisine=j['cuisine'], ingredients=[]) 
  for i in j['ingredients']:
    new_ingredient = Ingredients(ingredient=i)
    new_recipe.ingredients.append(new_ingredient)
    session.add(new_ingredient)
  session.add(new_recipe)

  session.commit()

f.close()

f=open('test.json', 'rb')
test_lines=''.join(f.readlines())
jtlines = json.loads(test_lines)

for jt in jtlines:
  #add recipe
  new_test_recipe = Test(recipe_id=jt['id'], ingredients=[]) 
  for i in jt['ingredients']:
    new_test_ingredient = Test_Ingredients(ingredient=i)
    new_test_recipe.ingredients.append(new_test_ingredient)
    session.add(new_test_ingredient)
  session.add(new_test_recipe)

  session.commit()

f.close()