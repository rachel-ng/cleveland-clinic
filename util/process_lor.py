import os
import glob 

from datetime import datetime
from util import image_conversion, extract_text

def get_find_box_args(processed_lor):
    """
    For using find rank boxes from selected boxes
    """

    page_src_args = (
        processed_lor['pdf'],
        processed_lor['ocr text full'],
        processed_lor['pngs']
    )

    return page_src_args


def get_lor_applicant(pdf_path):
    '''Extract text from LOR PDF and return dictionary with info from first line'''
    if (os.path.isfile(pdf_path)):
        extracted_text = extract_text.get_pdf_text(pdf_path)

        # get applicant info
        line = [i.strip() for i in extracted_text[0].split("\n", 1)[0].replace(")", "(").split("(")]
        applicant = {"name": line[0],
                     "id": line[1],
                     "author": line[2].split("-")[-1].strip()
                     }

        return applicant
    else:
        print("no such file at {}".format(pdf_path))
        return None


def process_lor_to_boxes(pdf_path, png_dest_path='/content/drive/MyDrive/DFG/LOR_Data/dev_data', det=False):
    '''Return processed '''

    elapsed = datetime.now()
    if (os.path.isfile(pdf_path)):
        # attempt to extract text from pdf
        if det: print("get extracted text from {}".format(pdf_path))
        extracted_text = extract_text.get_pdf_text(pdf_path)

        # get applicant info
        line = [i.strip() for i in extracted_text[0].split("\n", 1)[0].replace(")", "(").split("(")]
        applicant = {"name": line[0],
                     "id": line[1],
                     "author": line[2].split("-")[-1].strip()
                     }

        if det: print(line, "\n", applicant)

        # convert pdf to png, if pngs already exist at dest they won't be converted
        if det: print("convert pdf to pngs")
        ocr_text = []
        png_template, png_pages = image_conversion.convert_pdf_png(pdf_path, applicant['id'], png_dest_path)

        # ocr
        if det: print("ocr")
        for page_path in png_pages:
            ocr_text.append(extract_text.process_ocr(page_path))
            #print(ocr_text[-1])
        if det: print("ocr done")

        # ocr_text = the list of text information per detected textbox.

        # output
        processed_lor = {'applicant': applicant,
                         'pdf': pdf_path, 'pngs': png_pages,
                         'extracted text': extracted_text,
                         'ocr text': [[j['text'] for j in i] for i in ocr_text],
                         'ocr text full': ocr_text
                         }

        print("elapsed: {}s\n".format(datetime.now() - elapsed))

        return processed_lor

    else:
        print("no such file at {}".format(pdf_path))
        return None

