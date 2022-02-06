import os
import cv2 as cv
import numpy as np
from non_max_suppression import non_max_suppression


big_char_template_files = [x for x in os.listdir('colored_chars') if x[0] == 'b']
big_char_templates = [(template_file.split('.')[0], cv.imread('colored_chars/' + template_file, 0))
                      for template_file in big_char_template_files]

small_char_template_files = [x for x in os.listdir('colored_chars') if x[0] == 's']
small_char_templates = [(template_file.split('.')[0], cv.imread('colored_chars/' + template_file, 0))
                      for template_file in small_char_template_files]

gamestart_templates_files = ['_start.bmp']
gamestart_templates = [(template_file.split('.')[0], cv.imread('colored_chars/' + template_file, 0))
                       for template_file in gamestart_templates_files]

gameend_templates_files = ['_end.bmp', '_end2.bmp']
gameend_templates = [(template_file.split('.')[0], cv.imread('colored_chars/' + template_file, 0))
                       for template_file in gameend_templates_files]

clock_templates_files = ['clock.bmp', 'clockstart.bmp']
clock_templates = [(template_file.split('.')[0], cv.imread('colored_chars/' + template_file, 0))
                   for template_file in clock_templates_files]


def parse_cards(img_gray, templates, region=None):
    rects = []
    probs = []
    labels = []

    x1, y1, x2, y2 = region
    img_gray = img_gray[y1:y2, x1: x2]

    for (label, template) in templates:

        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.85
        loc = np.where(res >= threshold)
        w, h = template.shape[::-1]
        for loc1 in zip(*loc[::-1]):
            rects.append([loc1[0], loc1[1], loc1[0] + w, loc1[1] + h])
            probs.append(res[loc1[1], loc1[0]])
            labels.append(label)

    picks = non_max_suppression(np.array(rects), np.array(probs), overlapThresh=0.1)
    for rect in rects:
        rect[0] += x1
        rect[1] += y1
        rect[2] += x1
        rect[3] += y1
    result = [[rects[j], probs[j], labels[j]] for j in picks]
    return result


def visualize(img, result):
    img_new = img.copy()
    for ((x1, y1, x2, y2), prob, label) in result:
        cv.rectangle(img_new, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.putText(img_new, label[1] + '%2d' % (prob*100), (x1, y1), cv.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2, color=(0, 0, 0))

    cv.imwrite('res.png', img_new)


def parse_big_cards(img_gray):
    # 200: 500
    templates = big_char_templates
    region = [0, 200, 1041, 628]
    result = parse_cards(img_gray, templates, region)
    return result


def parse_small_cards(img_gray, who):
    templates = small_char_templates
    if who == 0:
        region = [350, 110, 650, 140]
    elif who == 1:
        region = [80, 178, 350, 208]
    elif who == 3:
        region = [650, 178, 920, 208]
    else:
        return []
    result = parse_cards(img_gray, templates, region)
    return result


def parse_clock(img_gray):
    regions = [
        [370, 50, 443, 113],
        [80, 145, 144, 208],
        [400, 240, 460, 300],
        [888, 145, 955, 208],
    ]
    for i, region in enumerate(regions):
        result = parse_cards(img_gray, [clock_templates[0]], region)
        is_start = bool(result) and bool(parse_cards(img_gray, [clock_templates[1]], region))
        if result:
            return i, is_start
    return None


def parse_game_start(img_gray):
    region = [446, 254, 561, 296]
    result = parse_cards(img_gray, gamestart_templates, region)
    return bool(result)


# def parse_game_end(img_gray):
#     regions = [
#         [493, 45, 521, 82],
#         [46, 179, 70, 213],
#         [35, 562, 64, 598],
#         [998, 181, 1024, 213]
#     ]
#     for region in regions:
#         result = parse_cards(img_gray, gameend_templates, region)
#         if result:
#             return True
#     return False


if __name__ == '__main__':
    import time
    img_rgb = cv.imread('images5/1644143563.9381034.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    t1 = time.time()
    result = parse_game_end(img_gray)
    t2 = time.time()
    print(t2 - t1)
    print(result)
    # print(len(result), result)
    # visualize(img_rgb, result)
