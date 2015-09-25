# -*- coding: utf-8 -*-
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy
import os.path
from PIL import Image
import selectivesearch
# from selectivesearch import *

"""
https://github.com/scikit-image/scikit-image/blob/master/skimage/segmentation/_felzenszwalb_cy.pyx
"""
SELECTIVESEARCH_SCALE = 100  # 255.0*3  # 1 ~ 255 ?
SELECTIVESEARCH_SIGMA = 2.2  # Gaussian filter
SELECTIVESEARCH_MIN_SIZE = 10
DELETE_SIMILR_INCLUDE = True


def main(image_path):
    input_file_name = os.path.basename(image_path)
    image_array = pre_process(image_path)

    candidates = selective(image_path)

    # draw rectangles on the original image
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(image_array)
    for (x, y, w, h) in candidates:
        rect = mpatches.Rectangle(
            (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

    # plt.show()

    out_file = "data/result/{0}.png".format(input_file_name)

    delete_similr = "__delete_similr" if DELETE_SIMILR_INCLUDE else ''
    out_file = "data/result/scale_{0}__sigma_{1}__minsize__{2}{3}/{4}.png".format(
        SELECTIVESEARCH_SCALE,
        SELECTIVESEARCH_SIGMA,
        SELECTIVESEARCH_MIN_SIZE,
        delete_similr,
        input_file_name
    )
    dirname = os.path.dirname(out_file)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    plt.savefig(out_file)


def pre_process(image_path):
    resize = (256, 256)
    image = Image.open(image_path)
    image = image.resize(resize, Image.ANTIALIAS)
    image_array = numpy.asarray(image)

    return image_array


def selective(image_path):
    # loading lena image

    image_array = pre_process(image_path)

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
        print('size')
        x, y, w, h = r['rect']
        print(r['size'])
        print(w*h)
        print(r['size'] == w*h)
        
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 2000 pixels
        # print('size')
        # print(r['size'])
        if r['size'] < 15*15:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        if w / h > 3 or h / w > 3:
            continue
        candidates.add(r['rect'])

    return post_process(candidates)


def post_process(candidates):

    if not DELETE_SIMILR_INCLUDE:
        return candidates
    print('aaaa')
    print(len(candidates))

    filterd_candidates = candidates.copy()
    for c in candidates:
        x, y, w, h = c

        for _x, _y, _w, _h in candidates:
            if x == _x and y == _y and w == _w and h == _h:
                continue

            if abs(x - _x) < 10 and \
               abs(y - _y) < 10 and \
               w * h - _w * _h < 30*30 and \
               w * h - _w * _h > 0:
                print('delete')
                print((_x, _y, _w, _h))
                filterd_candidates.discard((_x, _y, _w, _h))

    print('bbb')
    print(len(filterd_candidates))
    return filterd_candidates

def delete_min_size(candidates):
    
    filterd_candidates = candidates.copy()
    
    
    
if __name__ == "__main__":

    files = glob.glob('data/images/*.jpg')
    for image_path in files:
        main(image_path)
