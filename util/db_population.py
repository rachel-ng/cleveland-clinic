import sqlalchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

import util
from util.base import Base
from util.models import Author, Author_Record, Applicant, LOR_Data, LOR_Page, Page_Block

def add_applicant(session, entry):
    try:
        existing_entry = session.query(Applicant).get(entry.id)
        if existing_entry == None:
            session.add(entry)
            session.commit()
            return session.query(Applicant).get(entry.id) 
        else:
            # print("Applicant exists in database: {}".format(existing_entry))
            return False
    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding Applicant: {}".format(e))
        raise e

def add_author(session, entry):
    try:
        existing_entry = session.query(Author).get(entry.name)
        if existing_entry == None:
            session.add(entry)
            session.commit()
            return session.query(Author).get(entry.name)
        else:
            # print("Author exists in database: {}".format(existing_entry))
            return False
    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding Author: {}".format(e))
        raise e

def add_author_record(session, entry):
    try:
        if not entry.author_id: 
            author = session.query(Author).filter(Author.name == entry.name).one_or_none()
            if author == None:
                author = Author(name=entry.name, institution=entry.institution, position=entry.position)
                add_author(session, author)
            entry.author_id=author.name
            session.add(entry)
            session.commit()
            return session.query(Author_Record).get((entry.lor_id,entry.author_id))
        else:
            # print("Author_Record exists in database: {}".format(existing_entry))
            return False
    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding Author_Record: {}".format(e))
        raise e

def add_lor_data(session, entry):
    try:
        existing_entry = session.query(LOR_Data).filter(LOR_Data.pdf_path == entry.pdf_path).one_or_none()
        if existing_entry == None:
            session.add(entry)
            session.commit()
            return session.query(LOR_Data).filter(LOR_Data.id == entry.id).first()
        else:
            print("LOR_Data exists in database: {}".format(existing_entry))
            return False
    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding LOR_Data: {}".format(e))
        raise e

def add_lor_page(session, entry):
    try:
        existing_entry = session.query(LOR_Page).filter(LOR_Page.id == entry.id).one_or_none()
        if existing_entry == None:
            session.add(entry)
            session.commit()
            return session.query(LOR_Page).filter(LOR_Page.id == entry.id).first()
        else:
            # print("LOR_Page exists in database: {}".format(existing_entry))
            return False
    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding LOR_Page: {}".format(e))
        raise e

def add_page_block(session, entry):
    try:
        existing_entry = session.query(Page_Block).filter(Page_Block.id == entry.id).one_or_none()
        if existing_entry == None:
            session.add(entry)
            session.commit()
            return session.query(Page_Block).filter(Page_Block.id == entry.id).first()
        else:
            # print("Page_Block exists in database: {}".format(existing_entry))
            return False
    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding Page_Block: {}".format(e))
        raise e

