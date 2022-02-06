from PIL import Image
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def display1():
    img = np.array(Image.open('images4/16440712339.bmp'))

    def is_red(r, g, b):
        return r > g and r > b and r > 120 and g < 80 and b < 80

    def is_black(r, g, b):
        return r < 50 and g < 50 and b < 50

    def is_white(r, g, b):
        return r > 200 and g > 200 and b > 200

    def is_blue(r, g, b):
        return b > r and b - r > 20 and b > g and b - g > 20


    H, W = img.shape[:2]

    img2 = np.zeros_like(img)
    for y in range(H):
        for x in range(W):
            c = img[y, x]
            if is_red(*c):
                img2[y, x] = [255, 0, 0]
            elif is_blue(*c):
                img2[y, x] = [0, 0, 255]
            elif is_white(*c):
                img2[y, x] = [255, 255, 255]
            elif is_black(*c):
                img2[y, x] = [0, 0, 0]
            else:
                img2[y, x] = [0, 255, 0]

    plt.imshow(img2)
    plt.show()




