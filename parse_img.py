import os

import numpy as np

up_clock = [(386, 62, [255, 239, 184]), (431, 63, [254, 234, 152]), (389, 99, [183, 125, 63]), (426, 98, [220, 178, 103]), (385, 77, [235, 201, 122]), (427, 72, [229, 192, 114]), (406, 70, [237, 239, 237]), (391, 84, [219, 213, 205]), (422, 86, [211, 211, 212]), (406, 99, [197, 190, 184])]
left_clock = [(85, 156, [240, 204, 125]), (136, 156, [254, 234, 162]), (90, 166, [252, 226, 147]), (128, 165, [244, 210, 130]), (87, 186, [190, 135, 69]), (135, 186, [182, 123, 62]), (109, 204, [204, 155, 89]), (108, 165, [234, 244, 248]), (95, 180, [220, 216, 211]), (110, 196, [197, 190, 184]), (127, 181, [205, 200, 195])]
down_clock = [(409, 253, [254, 234, 144]), (455, 253, [254, 234, 146]), (433, 250, [254, 234, 144]), (410, 284, [186, 129, 65]), (455, 283, [190, 136, 70]), (429, 297, [205, 155, 89]), (430, 259, [237, 239, 237]), (417, 274, [221, 219, 216]), (448, 274, [214, 208, 199]), (432, 289, [197, 190, 184])]
right_clock = [(898, 159, [251, 221, 142]), (947, 159, [252, 226, 147]), (922, 157, [255, 241, 152]), (900, 183, [204, 156, 89]), (946, 181, [177, 116, 58]), (919, 202, [230, 194, 117]), (920, 163, [234, 245, 250]), (907, 179, [222, 221, 219]), (939, 180, [211, 202, 187]), (921, 194, [197, 190, 184])]




clocks = [up_clock, left_clock, down_clock, right_clock]

def is_same_color(a, b):
    for i in range(3):
        if abs(a[i] - b[i]) > 10:
            return False
    return True


def get_clock(img):
    def is_clock(clock_sample_points):
        for (x, y, c) in clock_sample_points:
            if not is_same_color(img[y, x], c):
                return False
        return True

    for i, clock in enumerate(clocks):
        if is_clock(clock):
            return i

    return None



# 442, 342
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# img = Image.open('images3/16440621932.bmp')
# print(get_clock(np.array(img)))

files = os.listdir('images3')
files = sorted(files)
rectangles = []
for clock in clocks:
    x0 = min(x for (x, y, _) in clock)
    y0 = min(y for (x, y, _) in clock)
    x1 = max(x for (x, y, _) in clock)
    y1 = max(y for (x, y, _) in clock)
    rectangles.append([x0, y0, x1, y1])

for file in files[::30]:
    _file = os.path.join('images3', file)
    img = np.array(Image.open(_file))
    who = get_clock(img)

    fig, ax = plt.subplots()
    ax.imshow(img)

    if who is not None:
        x0, y0, x1, y1 = rectangles[who]
        rect = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    plt.show()

