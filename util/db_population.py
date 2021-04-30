import sqlalchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

import util
from util.base import Base
from util.models import Author, Author_Record, Applicant, LOR_Data, LOR_Page, Page_Block

def add_applicant(session, entry, commit=False):
    try:
        existing_entry = session.query(Applicant).get(entry.id)
        if existing_entry == None:
            session.add(entry)

            if commit: 
                session.commit()
                return session.query(Applicant).get(entry.id) 
            else: 
                # added Applicant to session 
                return True
        else:
            # print("Applicant exists in database: {}".format(existing_entry))
            return False

    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding Applicant: {}".format(e))
        raise e

def add_author(session, entry, commit=False):
    try:
        existing_entry = session.query(Author).get(entry.name)
        if existing_entry == None:
            session.add(entry)

            if commit: 
                session.commit()
                return session.query(Author).get(entry.name)
            else: 
                # added Author to session 
                return True
        else:
            # print("Author exists in database: {}".format(existing_entry))
            return False

    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding Author: {}".format(e))
        raise e

def add_author_record(session, entry, commit=False):
    try:
        if not entry.author_id: 
            
            # add author_id to entry
            author = session.query(Author).filter(Author.name == entry.name).one_or_none()
            if author == None:
                # create Author if necessary 
                author = Author(name=entry.name, institution=entry.institution, position=entry.position)
                add_author(session, author, commit)

            existing_entry = session.query(Author_Record).get((entry.lor_id,entry.author_id))
            if existing_entry == None:
                entry.author_id=author.name
                session.add(entry)

                if commit: 
                    session.commit()
                    return session.query(Author_Record).get((entry.lor_id,entry.author_id))
                else: 
                    # added Author_Record to session 
                    return True

            else:
                # print("Author_Record exists in database: {}".format(existing_entry))
                return False

        else:
            # print("Author_Record exists in database: {}".format(existing_entry))
            return False
    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding Author_Record: {}".format(e))
        raise e

def add_lor_data(session, entry, commit=False):
    try:
        existing_entry = session.query(LOR_Data).filter(LOR_Data.pdf_path == entry.pdf_path).one_or_none()
        if existing_entry == None:
            session.add(entry)

            if commit: 
                session.commit()
                return session.query(LOR_Data).filter(LOR_Data.id == entry.id).first()
            else: 
                # added LOR_Data to session 
                return True

        else:
            print("LOR_Data exists in database: {}".format(existing_entry))
            return False

    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding LOR_Data: {}".format(e))
        raise e

def add_lor_page(session, entry, commit=False):
    try:
        existing_entry = session.query(LOR_Page).filter(LOR_Page.id == entry.id).one_or_none()
        if existing_entry == None:
            session.add(entry)

            if commit: 
                session.commit()
                return session.query(LOR_Page).filter(LOR_Page.id == entry.id).first()
            else: 
                # added LOR_Page to session 
                return True

        else:
            # print("LOR_Page exists in database: {}".format(existing_entry))
            return False

    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding LOR_Page: {}".format(e))
        raise e

def add_page_block(session, entry, commit=False):
    try:
        existing_entry = session.query(Page_Block).filter(Page_Block.id == entry.id).one_or_none()
        if existing_entry == None:
            session.add(entry)

            if commit: 
                session.commit()
                return session.query(Page_Block).filter(Page_Block.id == entry.id).first()
            else: 
                # added Page_Block to session 
                return True

        else:
            # print("Page_Block exists in database: {}".format(existing_entry))
            return False

    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print("ERROR when adding Page_Block: {}".format(e))
        raise e

