def select_match_ocr_textboxes(pdf_path, ocr_text, png_paths, match, det=False):
    """
    Find the form page with specific text on it
      used for rank and author extraction.
    """

    if det: print(ocr_text)

    # 'Cleveland Clinic Foundation Program, Plastic Surgery-Integrated Page 4\nA.ERAS-PDWS 06/21/2018\nConfidential - Do not disclose or distribute applicant information to persons outside the residency/fellowship application process. The applicant waived rights to view this LoR'],
    # something similar to this on every page
    # word applicant is on every page

    # 3/8: any to match https://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-python#comment36940464_6531704

    if det: print("{}{} pages".format("💀 " if len(ocr_text) < 2 else "", len(ocr_text)))

    # use joined text to quickly narrow down page with match rather than iterate through everything
    joined = [" ".join([j['text'] for j in i]) for i in ocr_text]
    selected = []
    # look for page with form
    for i in range(len(joined)):
        if any(s in joined[i] for s in match):
            for j in range(len(ocr_text[i])):
                # look for individual text blocks with strings found in match
                if any(s in ocr_text[i][j]["text"] for s in match):
                    if det and ("out of" in ocr_text[i][j]["text"] or "Out of" in ocr_text[i][j]["text"]):
                        print("🌟🌟🌟")
                    selected.append([i, j])

    return selected


def find_relevant_boxes_from_selected_boxes(selected, ocr_text):
    return [ocr_text[i[0]][i[1]] for i in selected]



