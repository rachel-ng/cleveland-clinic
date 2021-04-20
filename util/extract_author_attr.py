import process_lor
import string_match


def find_relevant_boxes_from_selected_boxes(selected, ocr_text):
  return [ocr_text[i[0]][i[1]] for i in selected]


def find_author_box_from_processed_lor(processed_lor):
    # First page of the form

    template = ['Reference provided by', 'Present Position', 'Institution']

    page_src_args = process_lor.get_find_box_args(processed_lor)
    author_boxes_idxs = string_match.select_match_ocr_textboxes(*page_src_args,
                                                   match=template)
    author_boxes = find_relevant_boxes_from_selected_boxes(author_boxes_idxs,
                                                           processed_lor['ocr text full'])

    assert len(author_boxes) == 1, 'Multiple locations detected for author information in PDF.'
    return author_boxes[0]


def find_author_info_from_box(author_box):
    """
    Accepts output of find_author_box_from_processed_lor
    """

    this_text = author_box['text']
    # This might be brittle, depending on how well OCR detects the printed text.

    templates = {
        'reference': 'Reference Provided By:',
        'reference end': 'Reference Letter ID#',
        'institution': 'Institution:',
        'position': 'Present Position:',
        'position end': 'Institution:',
        'institution end': 'Telephone #'
    }

    template_idxs = {
        k: this_text.find(templates[k])
        for k in templates
    }

    was_found = lambda x: x != -1
    assert all(map(was_found, template_idxs.values())), \
        'Could not find one of the author text attributes.'

    reference_idx_start = template_idxs['reference'] + len(templates['reference'])
    position_idx_start = template_idxs['position'] + len(templates['position'])
    institution_idx_start = template_idxs['institution'] + len(templates['institution'])

    author_attr = {
        'name': this_text[reference_idx_start:template_idxs['reference end']],
        'position': this_text[position_idx_start:template_idxs['position end']],
        'institution': this_text[institution_idx_start:template_idxs['institution end']],
    }

    author_attr = {k: v.strip() for k, v in author_attr.items()}

    return author_attr

