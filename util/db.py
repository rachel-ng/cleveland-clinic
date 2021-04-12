import sys, os, copy
from os.path import join, exists
import glob

import string
import re
import random

from datetime import datetime

from IPython.display import display
import pandas as pd

import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append('/content/drive/My Drive/DFG/util')

from base import Base
from models import Author, Author_Record, Applicant, LOR_Data, LOR_Page, Page_Block

ROOT_DIR = './drive/MyDrive/DFG/'  # root directory
DATA_DIR = os.path.join(ROOT_DIR, 'db_data')  # data directory -- changed data to db_data (nancy)
DB_FILE = os.path.join(DATA_DIR, 'data.db')  # db file



class DB:
    def __init__(self, db_file=DB_FILE):
        self.engine = create_engine("sqlite:///{}".format(db_file))
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        
    def __repr__(self):
        return "DB {}".format(self.engine) 

    def show_all(self):
        with self.Session.begin() as session:
            print(Applicant.__tablename__)
            display(pd.read_sql_table(Applicant.__tablename__, session.bind))

            print("\n\n")
            print(Author.__tablename__)
            display(pd.read_sql_table(Author.__tablename__, session.bind))

            print("\n\n")
            print(Author_Record.__tablename__)
            display(pd.read_sql_table(Author_Record.__tablename__, session.bind))

            print("\n\n")
            print(LOR_Data.__tablename__)
            display(pd.read_sql_table(LOR_Data.__tablename__, session.bind))

            print("\n\n")
            print(LOR_Page.__tablename__)
            display(pd.read_sql_table(LOR_Page.__tablename__, session.bind))

            print("\n\n")
            print(Page_Block.__tablename__)
            display(pd.read_sql_table(Page_Block.__tablename__, session.bind))
    


