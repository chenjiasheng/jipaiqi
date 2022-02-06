from PIL import Image, ImageOps
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def get_template1():
    def img_to_img2(img):
        img2 = np.average(img, axis=-1)
        img2 = (img2 > 230) * 255
        return img2

    img = np.array(Image.open('images4/16440712339.bmp'))
    height = 35
    width = 29
    x0 = 10
    y0 = 455
    stride = 72.8

    for i in range(14):
        x = x0 + int(i * stride)
        y = y0
        rect = img[y:y+height, x: x+width]
        rect = img_to_img2(rect)
        char_img = Image.fromarray(rect)
        char_img = char_img.convert('1')
        char_img.save(str(i) + '.bmp')


def get_template2():
    img = np.array(Image.open('images4/16440712339.bmp'))
    height = 35
    width = 29
    x0 = 10
    y0 = 455
    stride = 72.8

    for i in range(14):
        x = x0 + int(i * stride)
        y = y0
        rect = img[y:y + height, x: x + width]
        char_img = Image.fromarray(rect)
        char_img.save(str(i) + '.bmp')


def get_template3():
    img = np.array(Image.open('images3/16440623144.bmp'))
    height = 35
    width = 29
    x0 = 59
    y0 = 419
    stride = 81.9

    for i in range(12):
        x = x0 + int(i * stride)
        y = y0
        rect = img[y:y + height, x: x + width]
        char_img = Image.fromarray(rect)
        char_img.save(str(i) + '.bmp')


def get_template4():
    img = np.array(Image.open('images2/16440608578.bmp'))
    height = 27
    width = 22
    x0 = 889
    y0 = 180
    stride = 33.25

    for i in range(2):
        x = x0 + int(i * stride)
        y = y0
        rect = img[y:y + height, x: x + width]
        char_img = Image.fromarray(rect)
        char_img.save(str(i) + '.bmp')


def get_template5():
    img = np.array(Image.open('images2/16440608578.bmp'))
    height = 27
    width = 22
    x0 = 89
    y0 = 180
    stride = 33.25

    for i in range(6):
        x = x0 + int(i * stride)
        y = y0
        rect = img[y:y + height, x: x + width]
        char_img = Image.fromarray(rect)
        char_img.save(str(i) + '.bmp')

get_template4()
# get_template5()
