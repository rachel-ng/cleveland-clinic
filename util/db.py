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
from sqlalchemy import inspect, MetaData

import util
from util.base import Base
from util.models import Author, Author_Record, Applicant, LOR_Data, LOR_Page, Page_Block

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

    def add_all(self, entries):
        self.Session.add_all(entries)
        self.Session.commit()

    def display(self):
        """displays all tables as pandas dataframes"""

        with self.Session.begin() as session:
            inspector = inspect(self.engine)
            schemas = inspector.get_schema_names()
            main = [{table_name: inspector.get_columns(table_name, schema=schema) for table_name in inspector.get_table_names(schema=schema)} for schema in schemas]
            for i in main[0]:
                print(i)
                display(pd.read_sql_table(i, session.bind))
                print("\n\n")

    def all_dataframes(self):
        """returns dictionary of all tables as pandas dataframes"""

        with self.Session.begin() as session:
            inspector = inspect(self.engine)
            schemas = inspector.get_schema_names()
            main = [{table_name: inspector.get_columns(table_name, schema=schema) for table_name in inspector.get_table_names(schema=schema)} for schema in schemas]
            return {i:pd.read_sql_table(i, session.bind) for i in main[0]}



