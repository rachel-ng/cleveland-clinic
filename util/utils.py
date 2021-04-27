import os
import re

def png_name (pdf_path, applicant_id=None):
    """Converts pdf path name to png name."""
    if applicant_id:
        assert re.match("^\d{8}$",applicant_id) != None, '"{}" is not a valid applicant id'.format(applicant_id)

    # ./drive/MyDrive/DFG/LOR_Data/dev_data/Dept. Chair LoR - Author Name Split_19-20.pdf
    png_path = os.path.split(pdf_path)
    # ['./drive/MyDrive/DFG/LOR_Data/dev_data/', 'Dept. Chair LoR - Author Name Split_19-20.pdf']

    # Dept. Chair LoR - Author Name Split_19-20.pdf
    # get file name w/o text, get rid of spaces and other unsafe characters
    png_name = re.sub(r'(?u)[^-\w.]', '', png_path[1].replace(" ","_").split(".pdf")[0])

    # Dept._Chair_LoR_-_Author_Name_Split_19-20-00000000-%d.png
    return "{}{}-%d.png".format(png_name, "" if applicant_id == None else "-{}".format(applicant_id))


def lor_id (year, file_path):
    hashed = hash(file_path)
    return "{}_{}{}".format(year, 0 if hashed < 0 else "", abs(hashed))


