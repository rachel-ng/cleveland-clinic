import cv2
import datetime
import numpy as np

import process_lor
import string_match

def checkbox_crop(img,y1=0):
    return img[y1:img.shape[0], 0:img.shape[1]]

### function to fix image as binary
def fix(img):
    img[img > 127] = 255
    img[img < 127] = 0
    return img


def find_rank_boxes_from_selected_boxes(selected, pdf_path, ocr_text, png_paths):
    """
    Accepts the output of select_match_ocr_textboxes,
       with the correct rank string template passed in.
    """
    # go through list of pages + blocks
    for i in selected:
        name = png_paths[i[0]]
        y = ocr_text[i[0]][i[1]]["y"]
        cb = find_rank_boxes(name, checkbox_crop, y)
        print(cb)

    return cb

def find_rank_from_processed_lor(processed_lor):

  template = ["rank this applicant","would not rank","20 applicants"]
  page_src_args = process_lor.get_find_box_args(processed_lor)

  rank_boxes = string_match.select_match_ocr_textboxes(*page_src_args,
                                          match = template)
  rank = find_rank_boxes_from_selected_boxes(rank_boxes, *page_src_args)

  return rank

def find_rank_boxes(img_path, img_crop_func=False, y=0, cb_leeway=5, det=False):
    start = datetime.now()
    if img_crop_func:
        image = img_crop_func(cv2.imread(img_path), y)
    else:
        image = cv2.imread(img_path)

    ### binarising image
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th1, img_bin = cv2.threshold(gray_scale, 150, 225, cv2.THRESH_BINARY)

    # vertical and horizontal kernels
    lineWidth = 1
    lineMinWidth = 20

    kernal1 = np.ones((lineWidth, lineWidth), np.uint8)
    kernal1h = np.ones((1, lineWidth), np.uint8)
    kernal1v = np.ones((lineWidth, 1), np.uint8)

    kernal6 = np.ones((lineMinWidth, lineMinWidth), np.uint8)
    kernal6h = np.ones((1, lineMinWidth), np.uint8)
    kernal6v = np.ones((lineMinWidth, 1), np.uint8)

    # detect horizontal lines
    img_bin_h = cv2.morphologyEx(~img_bin, cv2.MORPH_CLOSE, kernal1h)  # bridge small gap in horizonntal lines
    img_bin_h = cv2.morphologyEx(img_bin_h, cv2.MORPH_OPEN,
                                 kernal6h)  # kep ony horiz lines by eroding everything else in hor direction
    # cv2_imshow(img_bin_h)

    ## detect vertical lines
    img_bin_v = cv2.morphologyEx(~img_bin, cv2.MORPH_CLOSE, kernal1v)  # bridge small gap in vert lines
    img_bin_v = cv2.morphologyEx(img_bin_v, cv2.MORPH_OPEN,
                                 kernal6v)  # kep ony vert lines by eroding everything else in vert direction
    # cv2_imshow(img_bin_v)

    # merge vertical + horizontal lines for blocks
    img_bin_final = fix(fix(img_bin_h) | fix(img_bin_v))

    finalKernel = np.ones((5, 5), np.uint8)
    img_bin_final = cv2.dilate(img_bin_final, finalKernel, iterations=1)

    # cv2_imshow(img_bin_final)

    # "Apply Connected component analysis on the binary image to get the blocks required."
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)

    print("{} blocks found".format(len(stats)))

    img_cp = image.copy()
    cb = 0
    dct = []
    ### skipping first two stats as background
    for x, y, w, h, area in stats[2:]:
        if area > 50:
            avg = np.array(cv2.mean(img_cp[y:y + h, x:x + w])).astype(np.uint8)

            if det:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if avg[0] < 255 - cb_leeway:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    if False:
                        cv2.imshow(img_cp[y:(y + h), x:(x + w)])
                        print('{}\taverage color (BGR): {}'.format(cb, avg))
                        print("\tx: {}, {}, y: {}, {}\t\tw: {}, h: {}, area: {}".format(x, x + w, y, y + h, w, h, area))

                if len(stats) < 100:
                    cv2.putText(image, str(cb), (x - 10, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                elif avg[0] < 255 - cb_leeway:
                    cv2.putText(image, str(cb), (x - 10, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            dct.append({"x": x, "x2": x + w,
                        "y": y, "y2": y + h,
                        "w": w, "h": h,
                        "area": area,
                        "index": cb,
                        "has_check": avg[0] < 255 - cb_leeway,
                        "avg": avg
                        })

            cb += 1

    if det: cv2_imshow(image)
    dct = sorted(dct, key=lambda i: (i['x'] * i['x']) + (i['y'] * i['y']))

    print("find rank boxes: {}s".format(datetime.now() - start))

    return dct
