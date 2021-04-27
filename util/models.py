import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy import Boolean, PickleType, DateTime, Float
from sqlalchemy.orm import relationship, backref

import util
from util.base import Base


class Applicant(Base):
    __tablename__ = "applicant_data"

    id = Column(String(8), primary_key=True)
    name = Column(String, nullable=False)
    year = Column(String, nullable=False)
    institution = Column(String)
    race = Column(String)
    gender = Column(String)

    lors = relationship("LOR_Data", back_populates="applicant")

    def __repr__(self):
        repr_items = self.id, self.name, self.year, self.institution
        repr_str = "Applicant " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

class Author(Base):
    __tablename__ = "author_data"

    name = Column(String, primary_key=True)
    institution = Column(String)
    position = Column(String)

    records = relationship("Author_Record", back_populates="author")

    def __repr__(self):
        repr_items = self.name, self.institution, self.position
        repr_str = "Author " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

class Author_Record(Base):
    __tablename__ = "author_record_data"

    name = Column(String, nullable=False, primary_key=True)
    year = Column(String, nullable=False)
    institution = Column(String)
    position = Column(String)
    origin = Column(String)
    lor_id = Column(String, ForeignKey("lor_data.id"), primary_key=True)
    author_id = Column(String, ForeignKey("author_data.name"))

    lor = relationship("LOR_Data", back_populates="authors")
    author = relationship("Author", back_populates="records")

    def __repr__(self):
        repr_items = self.name, self.year, self.institution, self.position, self.lor_id, self.author_id
        repr_str = "Author_Record " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

class LOR_Data(Base):
    __tablename__ = "lor_data"

    id = Column(String, primary_key=True) 
    applicant_id = Column(String, ForeignKey("applicant_data.id"), nullable=False)
    pdf_path = Column(String, nullable=False)
    png_template = Column(String, nullable=False)
    pages = Column(Integer)
    institution = Column(String)
    form_rank = Column(String)

    applicant = relationship("Applicant", back_populates="lors")
    authors = relationship("Author_Record", back_populates="lor")
    lor_pages = relationship("LOR_Page", back_populates="lor_file")

    def __repr__(self):
        repr_items = self.id, self.applicant_id, self.pdf_path, self.png_template, self.pages, self.institution
        repr_str = "LOR_Data " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

class LOR_Page(Base):
    __tablename__ = "lor_page_data"

    id = Column(String, primary_key=True) 
    lor_id = Column(String, ForeignKey("lor_data.id"), nullable=False)
    png_path = Column(String, nullable=False)
    page_number = Column(Integer)
    blocks = Column(Integer)
    form = Column(Boolean, default=False)
    rank = Column(Boolean, default=False)
    signature = Column(Boolean, default=False) 
    ocr_text = Column(String)
    processed_text = Column(String)

    lor_file = relationship("LOR_Data", back_populates="lor_pages") 
    page_blocks = relationship("Page_Block", back_populates="lor_page") 

    def __repr__(self):
        repr_items = self.id, self.lor_id, self.png_path, self.page_number, self.blocks, self.form, self.rank, self.ocr_text.replace("\n"," "), self.processed_text.replace("\n"," ")
        repr_str = "LOR_Page " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

class Page_Block(Base):
    __tablename__ = "page_block_data"

    id = Column(String, primary_key=True)
    page_id = Column(String, ForeignKey("lor_page_data.id"), nullable=False)
    block_number = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    w = Column(Integer, nullable=False)
    h = Column(Integer, nullable=False)
    
    lor_page = relationship("LOR_Page", back_populates="page_blocks") 

    def __repr__(self):
        repr_items = self.id, self.page_id, self.block_number, self.x, self.y, self.w, self.h, self.text.replace("\n"," ")
        repr_str = "Page_Block " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)


