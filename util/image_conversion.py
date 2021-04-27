import os
import re
import glob
import subprocess

from os.path import join, exists

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


def convert_pdf_png(pdf_path, applicant_id=None, dest_path=None):
    """Convert pdf to png, one picture for each page."""

    if (os.path.isfile(pdf_path)):

        png_template = png_name(pdf_path, applicant_id)
        png_path = join(dest_path if dest_path else os.path.split(pdf_path)[0], png_template)

        # escape spaces in filename for subprocess
        pdf_path = pdf_path.replace(" ", "\\ ")

        # check whether pdf has already been converted
        if len(glob.glob(png_path.replace("%d", "*"))) == 0: 
            cmd = "gs -dSAFER -r300 -sDEVICE=png16m -o {} {}    ".format(png_path, pdf_path)
            #print("png name: {}\n\npdf: {}\npng: {}\ncmd: {}\n".format(png_template, pdf_path, png_path, cmd))

            subprocess.run(cmd, shell=True, stdout=True)

            cmd_test = 'test -f /etc/resolv.conf && echo "{} exists."'.format(pdf_path)
            subprocess.run(cmd_test, shell=True, stdout=True)

        result_path = glob.glob(png_path.replace("%d", "*"))

        return png_path, result_path  # return paths of converted files

    else:
        print("no such file at {}".format(pdf_path))
        return None

