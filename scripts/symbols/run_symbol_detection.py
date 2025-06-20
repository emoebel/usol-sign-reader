from signreader.engine.symbol import SymbolDetector
import signreader.utils.io as io
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import signreader.utils.plot as plot

# YOLO test set:
#path_output = '/Users/manu/boulot/unit_solutions/predictions/symbol_detection/yolo_test_set/'
#path_images = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/yolo/images/val/'
#fname_list = io.get_fname_list_from_dir_bis(path_images, ext_list=['jpg', 'jpeg', 'png'], with_extension=True)

# Cellpose test set:
path_output = '/Users/manu/boulot/unit_solutions/predictions/symbol_detection/cellpose_test_set/'
path_images = '/Users/manu/boulot/unit_solutions/data/datasets/segmentation/cellpose/test/'
fname_list = io.get_fname_list_from_dir_bis(path_images, ext_list=['jpg'], with_extension=True) # images are all jpg here. Masks are png

symbdetector = SymbolDetector()

for idx, fname in enumerate(fname_list):
    print(f'Processing image {idx+1}/{len(fname_list)}: {fname}')
    img_np = np.asarray(Image.open(path_images + fname))
    boxes, class_names = symbdetector(img_np)

    fig, ax = plt.subplots(1, 1)
    plot.plot_bounding_boxes(ax, img_np, boxes, class_names)

    fname_no_ext = os.path.splitext(fname)[0]
    fig.set_figheight(15)
    fig.set_figwidth(15)
    fig.tight_layout()
    fig.savefig(path_output + fname_no_ext + '.png')