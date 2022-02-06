import numpy as np
from pynput import mouse

off_x, off_y = 5, 163
points = []

from PIL import Image
img = np.array(Image.open('images4/16440711897.bmp'))



import webcolors

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name




def on_click(x, y, button, pressed):


    print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
    if button == mouse.Button.right:
        return False

    if not pressed:
        return

    img_x, img_y = x - off_x, y - off_y
    color = list(img[img_y, img_x])
    actual_name, closest_name = get_colour_name(color)
    print("Actual colour name:", actual_name, ", closest colour name:", closest_name)

    # points.append((img_x, img_y, color))


# Collect events until released
with mouse.Listener(
        on_move=None,
        on_click=on_click,
        on_scroll=None) as listener:
    listener.join()

print(points)



