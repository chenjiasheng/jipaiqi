import os

import cv2
import numpy as np
from PIL import Image

chars = 'j2AKQJt9876543rRSBHCD'

height = 35
width = 29
x0 = 10
y0 = 455
stride = 72.8

WHITE = True
BLACK = False

def rgb_to_gray(rgb):
    return np.average(rgb, axis=-1).astype('uint8')

def gray_to_bin(gray):
    bin = gray > 230
    return bin


big_cards = [np.array(Image.open(os.path.join('binary_chars', str(card)+'.bmp'))) for card in range(14)]

def card_sim(img, x, y, card):
    rect = img[y: y + height, x: x + width]
    return np.sum(rect == card) / (height * width)

def parse_self_cards(img):
    result = []
    visited = np.zeros_like(img, dtype=bool)
    for x in range(0, 980):
        for y in range(230, 472):
            if visited[y, x]:
                continue
            if img[y, x] is False:
                continue
            card_sims = [card_sim(img, x, y, card) for card in big_cards]
            card = np.argmax(card_sims)
            sim = card_sims[card]
            if sim > 0.9:
                result.append([x, y, width, height, card])
                visited[max(0, y-height): y+height, max(0, x-width): x+width] = True

    return result


def parse_self_cards2():
    import cv2 as cv
    import numpy as np
    from imutils.object_detection import non_max_suppression

    from matplotlib import pyplot as plt
    img_rgb = cv.imread('images3/16440621932.bmp')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    templates = [cv.imread('colored_chars/%d.bmp'%i, 0) for i in range(17)]

    result = []


    for i, template in enumerate(templates):
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(res >= threshold)
        w, h = template.shape[::-1]
        rects = [[loc1[0], loc1[1], loc1[0] + w, loc1[1] + h] for loc1 in zip(*loc[::-1])]
        rects = non_max_suppression(np.array(rects))

        for x1, y1, x2, y2 in rects:
            cv.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.putText(img_rgb, chars[i], (x1, y1), cv.FONT_HERSHEY_SIMPLEX, fontScale=0.7, thickness=2, color=(0, 255, 0))
            result.append([[x1, y1, x2, y2], i])

    cv.imwrite('res.png', img_rgb)
    print(len(result), result)

    rects = np.array([x[0] for x in result])
    rects = non_max_suppression(np.array(rects))
    print(len(rects))
    assert len(result) == len(rects)


def parse_self_cards3():
    import MTM
    from MTM import matchTemplates
    import cv2 as cv

    listTemplate = [(str(i), cv.imread('colored_chars/%d.bmp' % i, 0)) for i in range(22)]
    rgb_img = cv.imread('images3/16440621932.bmp')
    input_img = cv.cvtColor(rgb_img, cv.COLOR_BGR2GRAY)

    hits = matchTemplates(listTemplate,
                          input_img,
                          score_threshold=0.9,
                          searchBox=(0, 0, 3000, 750),
                          method=cv2.TM_CCOEFF_NORMED,
                          maxOverlap=0.1)

    overlay = MTM.drawBoxesOnRGB(rgb_img,
                             hits,
                             showLabel=True,
                             labelColor=(255, 0, 0),
                             boxColor=(0, 0, 255),
                             labelScale=1,
                             boxThickness=3)
    cv.imwrite('res2.png', overlay)
    print(len(hits))



import time
t1 = time.time()
parse_self_cards2()
print(time.time() - t1)
#
#
# img = np.array(Image.open('images4/16440712339.bmp'))
# img2 = gray_to_bin(rgb_to_gray(img))
# result = parse_self_cards(img2)
# print(result)
#
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# fig, ax = plt.subplots()
# ax.imshow(img)
# for (x, y, w, h, i) in result:
#     rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='g', facecolor='none')
#     ax.add_patch(rect)
#     ax.text(x, y, chars[i], color='g')
#
# plt.show()
#
#
#
