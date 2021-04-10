import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy import Boolean, PickleType, DateTime, Float
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Author(Base):
    __tablename__ = "author_data"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    institution = Column(String)
    position = Column(String)

    records = relationship("Author_Record", back_populates="author")

    def __repr__(self):
        # return "Author {} {} {} {}".format(self.id, self.name, self.institution, self.position)
        repr_items = self.id, self.name, self.institution, self.position
        repr_str = "Author " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

class Author_Record(Base):
    __tablename__ = "author_record_data"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(String, nullable=False)
    institution = Column(String)
    position = Column(String)
    lor_id = Column(String, ForeignKey("lor_data.id"), nullable=False)
    author_id = Column(String, ForeignKey("author_data.id"))

    lor = relationship("LOR_Data", back_populates="authors")
    author = relationship("Author", back_populates="records")

    def __repr__(self):
        # return "Author_Record {} {} {} {}".format(self.id, self.name, self.institution, self.position, self.lor_id, self.author_id)
        repr_items = self.id, self.name, self.year, self.institution, self.position, self.lor_id, self.author_id
        repr_str = "Author_Record " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

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
        # return "Applicant {} {} {} {}".format(self.id, self.name, self.year, self.institution)
        repr_items = self.id, self.name, self.year, self.institution
        repr_str = "Applicant " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

class LOR_Data(Base):
    __tablename__ = "lor_data"

    id = Column(String, primary_key=True) # lor_id
    applicant_id = Column(String, ForeignKey("applicant_data.id"), nullable=False)
    pdf_path = Column(String, nullable=False)
    png_template = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    institution = Column(String)
    form_rank = Column(String)

    applicant = relationship("Applicant", back_populates="lors")
    authors = relationship("Author_Record", back_populates="lor")
    lor_pages = relationship("LOR_Page", back_populates="lor_file")

    def __repr__(self):
        # return "LOR_Data {} {} {} {} {} {} {}".format(self.id, self.applicant_id, self.pdf_path, self.png_template, self.pages, self.institution)
        repr_items = self.id, self.applicant_id, self.pdf_path, self.png_template, self.pages, self.institution
        repr_str = "LOR_Data " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

class LOR_Page(Base):
    __tablename__ = "lor_page_data"

    id = Column(String, primary_key=True) # lor_page_data.id
    lor_id = Column(String, ForeignKey("lor_data.id"), nullable=False)
    png_path = Column(String, nullable=False)
    page_number = Column(Integer)
    blocks = Column(Integer)
    form = Column(Boolean, default=False)
    rank = Column(Boolean, default=False)
    signature = Column(Boolean, default=False) 
    ocr_text = Column(String, nullable=False)

    lor_file = relationship("LOR_Data", back_populates="lor_pages") 
    page_blocks = relationship("Page_Block", back_populates="lor_page") 
    processed_page = relationship("Processed_Page", uselist=False, back_populates="lor_page") 

    def __repr__(self):
        # return "LOR_Page {} {} {} {} {} {} {} '{}'".format(self.id, self.lor_id, self.png_path, self.page_number, self.blocks, self.form, self.rank, self.ocr_text.replace("\n"," "))
        repr_items = self.id, self.lor_id, self.png_path, self.page_number, self.blocks, self.form, self.rank, self.ocr_text.replace("\n"," ")
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
        # return "Page_Block {} {} {} {} {} {} {} '{}'".format(self.id, self.page_id, self.block_number, self.x, self.y, self.w, self.h, self.text.replace("\n"," "))
        repr_items = self.id, self.page_id, self.block_number, self.x, self.y, self.w, self.h, self.text.replace("\n"," ")
        repr_str = "Page_Block " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

class Processed_Page(Base):
    __tablename__ = "processed_page_data"

    id = Column(String, primary_key=True)
    page_id = Column(String, ForeignKey("lor_page_data.id"), nullable=False)
    processed_text = Column(String, nullable=False)

    lor_page = relationship("LOR_Page", back_populates="processed_page") 

    def __repr__(self):
        # return "Processed_Page {} {} '{}'".format(self.id, self.page_id, self.processed_text.replace("\n"," "))
        repr_items = self.id, self.page_id, self.processed_text.replace("\n"," ")
        repr_str = "Processed_Page " + ("{} "*len(repr_items))
        return repr_str.format(*repr_items)

