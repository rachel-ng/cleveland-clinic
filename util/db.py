import sys, os, copy
from os.path import join, exists
import glob

import string
import re
import random

from datetime import datetime

import pandas as pd

import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect, MetaData
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy import Boolean, PickleType, DateTime, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func, distinct
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


sys.path.append('/content/drive/My Drive/DFG/util')

from utils import *
from models import *

# abs paths
DEV_DATA_PATH = './drive/MyDrive/DFG/LOR Data/dev_data'
LOR_PDFS_PATH = './drive/MyDrive/DFG/LOR Data/all_data/LOR PDFs' 

ROOT_DIR = './drive/MyDrive/DFG/'  # root directory

# files 
DATA_DIR = os.path.join(ROOT_DIR, 'db_data')  # data directory -- changed data to db_data (nancy)
DB_FILE = os.path.join(DATA_DIR, 'data.db')  # db file


Base = declarative_base()

def session_factory(DB_FILE=DB_FILE):
    engine = create_engine("sqlite:///{}".format(DB_FILE))
    Base.metadata.create_all(engine)
    _SessionFactory = sessionmaker(bind=engine)
    return engine, _SessionFactory()



