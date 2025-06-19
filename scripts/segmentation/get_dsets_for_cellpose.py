import signreader.utils.io as io
import signreader.utils.transform as tf
import numpy as np
import os
from PIL import Image

path_images = '/Users/manu/boulot/unit_solutions/data/images/all/'
path_segmaps = '/Users/manu/boulot/unit_solutions/data/annotations/segmentation/segmentation_maps/'

path_dset = '/Users/manu/boulot/unit_solutions/data/datasets/segmentation/cellpose/'

fname_list = io.get_fname_list_from_dir(path_segmaps, ext='npy')

# Random split to obtain train and test dsets:
len_dset_train = 400
len_dset_test = 100

rnd_idx_list = np.random.permutation(len(fname_list))

idx_list_train = rnd_idx_list[:len_dset_train]
idx_list_test = rnd_idx_list[len_dset_train:]

fname_list_train = []
for idx in idx_list_train:
    fname_list_train.append(fname_list[idx])
fname_list_test = []
for idx in idx_list_test:
    fname_list_test.append(fname_list[idx])

# Save split as txt files:
io.save_fname_list_to_txt(fname_list_train, path_dset + 'fname_list_train.txt')
io.save_fname_list_to_txt(fname_list_test, path_dset + 'fname_list_test.txt')


def create_dset(destination_folder, fname_list):
    # if not os.path.exists(path_dset + destination_folder):
    #     os.makedirs(path_dset + destination_folder)
    os.makedirs(path_dset + destination_folder)

    for fname in fname_list:
        print(destination_folder + fname)

        # Read image and copy to destination. Source files have different extensions, we want dest files to all be jpg
        fname_img_source = path_images + fname
        fname_img_dest = path_dset + destination_folder + fname + '.jpg'

        try:
            img = io.open_img_as_np_array(fname_img_source + '.jpg')
        except FileNotFoundError:
            try:
                img = io.open_img_as_np_array(fname_img_source + '.jpeg')
            except FileNotFoundError:
                #img = io.open_img_as_np_array(fname_img_source + '.png')
                rgba_image = Image.open(fname_img_source + '.png')
                rgb_image = rgba_image.convert('RGB')
                img = np.asarray(rgb_image)

        # Read segmentation map and copy to destination:
        fname_segmap_source = path_segmaps + fname + '.npy'
        fname_segmap_dest = path_dset + destination_folder + fname + '_masks.png'

        seg_map = np.load(fname_segmap_source)

        # Apply size normalisation and save:
        img_new, seg_map_new = tf.normalize_image_size(img, seg_map, min_size=512)

        io.save_np_array_as_img(fname_img_dest, img_new)
        io.save_np_array_as_img(fname_segmap_dest, seg_map_new)



create_dset(
    destination_folder='train/',
    fname_list=fname_list_train
)
create_dset(
    destination_folder='test/',
    fname_list=fname_list_test
)