import os
import cv2

import pdfplumber
import pytesseract
from pytesseract import Output


# From Tao
def get_pdf_text(pdf_path):
    '''Function that uses pdfplumber to extract text for each page in a pdf.'''
    if(os.path.isfile(pdf_path)):
        with pdfplumber.open(pdf_path) as pdf:
            return [page.extract_text() for page in pdf.pages]
    else:
        return None


def process_ocr(pdf_path, det=False):
    '''Identifies sections of text and OCRs them (reads them in) given a pdf path.'''
    if (os.path.isfile(pdf_path)):
        img = cv2.imread(pdf_path)
        d = pytesseract.image_to_data(img, output_type=Output.DICT)

        # 3/6: https://medium.com/@reiyasu/converting-images-to-text-with-pytesseract-and-opencv-in-python-20a0254120a7
        # 3/6: https://www.tomrochette.com/tesseract-tsv-format

        # 1: page, 2: block, 3: paragraph, 4: line, 5: word

        if det:
            for i in [i for i, e in enumerate(d['level']) if e == 2]:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
                cv2.putText(img, "({},{})".format(x, y), (x - 10, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            for i in [i for i, e in enumerate(d['level']) if e == 3]:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        block_boxes = [i for i, e in enumerate(d['level']) if e == 2]
        # [start,end] of a block, for all blocks + the end block because it got excluded :((
        ind_blocks = [[block_boxes[i], block_boxes[i + 1]] for i in range(len(block_boxes)) if
                      i < len(block_boxes) - 1] + [[block_boxes[-1], len(d['level'])]]
        # joins list splice of a block with a space between each item
        blocks = [{'text': " ".join([k for k in d['text'][i[0]:i[1]] if k != ""]).strip(), 'x': d['left'][i[0]],
                   'y': d['top'][i[0]], 'w': d['width'][i[0]], 'h': d['height'][i[0]]} for i in ind_blocks]

        if det: cv2.imshow(img)
        return [i for i in blocks if i['text'] != ""]

    else:
        print("no such file at {}".format(pdf_path))
        return None
