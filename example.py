# -*- coding: utf-8 -*-

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
from selectivesearch import *

from PIL import Image
import numpy

SELECTIVESEARCH_SCALE = 255.0  # 1 ~ 255
SELECTIVESEARCH_SIGMA = 0.1
SELECTIVESEARCH_MIN_SIZE = 10*10


def main(image_path):
    image = Image.open(image_path)
    image_array = pre_selective(image_path)

    candidates = selective(image_path)

    # draw rectangles on the original image
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(image_array)
    for (x, y, w, h) in candidates:
        rect = mpatches.Rectangle(
            (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

    # plt.show()
    plt.savefig("data/result.png")


def pre_selective(image_path):
    resize = (256, 256)
    image = Image.open(image_path)
    image = image.resize(resize, Image.ANTIALIAS)
    image_array = numpy.asarray(image)

    return image_array


def selective(image_path):
    # loading lena image

    image_array = pre_selective(image_path)

    # perform selective search
    # img = selectivesearch._generate_segments(
    #     image_array,
    #     scale=SELECTIVESEARCH_SCALE,
    #     sigma=SELECTIVESEARCH_SIGMA,
    #     min_size=SELECTIVESEARCH_MIN_SIZE
    # )
    # print('seg')
    # print(img)

    
    img_lbl, regions = selectivesearch.selective_search(
        image_array,
        scale=SELECTIVESEARCH_SCALE,
        sigma=SELECTIVESEARCH_SIGMA,
        min_size=SELECTIVESEARCH_MIN_SIZE
    )

    candidates = set()
    for r in regions:
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 2000 pixels
        # print('size')
        # print(r['size'])
        if r['size'] < 20*20:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        if w / h > 1.5 or h / w > 1.5:
            continue
        candidates.add(r['rect'])

    return post_selective(candidates)



def post_selective(candidates):

    if True:
        return candidates
    print('aaaa')
    print(len(candidates))
    
    filterd_candidates = candidates.copy()
    for c in candidates:
        x, y, w, h = c

        for _x, _y, _w, _h in candidates:
            if x == _x and y == _y and w == _w and h == _h:
                continue

            # print('exec')
            # print(abs(x - _x))
            # print(abs(y - _y))
            # print(abs(w * h - _w * _h))
            if abs(x - _x) < 50 and \
               abs(y - _y) < 50 and \
               abs(w * h - _w * _h) < 20*20:
                print('delete')
                print((_x, _y, _w, _h))
                filterd_candidates.discard((_x, _y, _w, _h))

    print('bbb')
    print(len(filterd_candidates))
    
    return filterd_candidates
    

if __name__ == "__main__":
    img_path = 'example.jpg'
    main(img_path)
