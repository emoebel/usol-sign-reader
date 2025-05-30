# This script is to get average image size in dataset, to determine which subsampling is to be used for cellpose.

import utils.io as io
import numpy as np
import matplotlib.pyplot as plt

path_polygons = '/Users/manu/boulot/unit_solutions/data/annotations/segmentation/napari_polygons'
path_images = '/Users/manu/boulot/unit_solutions/data/images/all/'

fname_list = io.get_fname_list_from_dir(path_polygons, 'csv')

img_shape_list = []
for fname in fname_list:
    print(fname)
    # Get img shape:
    try:
        img = io.open_img_as_np_array(path_images + fname + '.jpg')
    except FileNotFoundError:
        try:
            img = io.open_img_as_np_array(path_images + fname + '.jpeg')
        except FileNotFoundError:
            img = io.open_img_as_np_array(path_images + fname + '.png')

    img_shape = np.sort( img.shape[:2] )
    img_shape_list.append(img_shape)

img_shape_array = np.array(img_shape_list)

n_bins = 30
fig, axes = plt.subplots(nrows=1, ncols=2)
axes[0].hist(img_shape_array[:,0], bins=n_bins)
axes[0].grid(True)
axes[0].set_xlabel('Image size axe 0')
axes[1].hist(img_shape_array[:,1], bins=n_bins)
axes[1].grid(True)
axes[1].set_xlabel('Image size axe 1')
fig.savefig('dset_average_img_size.png')  # for visu