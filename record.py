import win32gui
import wscreenshot
import numpy as np
import time
import cv2
from PIL import Image
import os

dest_dir = 'images4'
win_text = '天天爱掼蛋'

ws = None
try:
    ws = wscreenshot.Screenshot(win_text)
except Exception:
    print('error: window not found.')
    exit(-1)

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

while True:
    img = ws.screenshot()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img.save(os.path.join(dest_dir, str(int(time.time() * 10)) + '.bmp'))
    time.sleep(0.1)

