import numpy as np

from scipy.misc import imsave
from PIL import Image
from os import walk
from os.path import join


def get_light_from_rgb(rgb):
    r, g, b = rgb
    maxc = max(r, g, b)
    minc = min(r, g, b)
    l = (minc + maxc) * 0.001960784
    return l


def read_array_from_pic(path):
    im = Image.open(path)
    rgb = np.array(im, dtype=np.float32)
    im = im.convert('L')
    l = np.array(im, dtype=np.float32)
    return rgb, l


def filter_low_light(l, count):
    low_light_value = 80
    if count % 10 == 0:
        low_light_value = 120
    l[l < low_light_value] = 0
    l[:][1800:] = 0
    # return np.nonzero(l)
    # return np.where(l == 0)
    return l


def create_pic(rgb, l):
    r, g, b = rgb.T
    rgb[np.where(l == 0)] = 0
    rgba = np.array([r, g, b, l.T]).T
    # img = Image.fromarray(rgba, mode='RGBA')
    # img = Image.fromarray(rgb)
    imsave('./save.png', rgba)


def add_star_track(from_dir, to_dir):
    count = 0
    for i in range(6333, 6582):
        from_name = 'IMG_' + str(i) + '.JPG'
        from_path = join(from_dir, from_name)
        to_path = join(to_dir, from_name)
        rgb, l = read_array_from_pic(from_path)
        last_name = 'IMG_' + str(i-1) + '.JPG'
        last_path = join(to_dir, last_name)
        rgb_temp, l_temp = read_array_from_pic(last_path)
        l_temp = filter_low_light(l_temp, count)
        count += 1
        rep = np.where(l_temp != 0)
        rgb[rep] = rgb_temp[rep]
        imsave(to_path, rgb)


if __name__ == '__main__':
    from_dir = '/path/to/from/dir'
    to_dir = '/path/to/save/dir'
    add_star_track(from_dir, to_dir)
