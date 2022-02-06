from PIL import Image
import numpy as np
import cv2
import os

npy_files = os.listdir('images')
for npy_file in npy_files:
    arr = np.load('images/' + npy_file)
    img = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img.save('images/' + npy_file.split('.')[0] + '.bmp')

