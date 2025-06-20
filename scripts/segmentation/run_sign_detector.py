from signreader.engine.sign import SignDetector
import signreader.utils.io as io
import signreader.utils.transform as transform
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

# Cellpose test set:
path_output = '/Users/manu/boulot/unit_solutions/predictions/sign_detection/cellpose_test_set/'
path_images = '/Users/manu/boulot/unit_solutions/data/datasets/segmentation/cellpose/test/'
fname_list = io.get_fname_list_from_dir_bis(path_images, ext_list=['jpg'], with_extension=True) # images are all jpg here. Masks are png

signdetector = SignDetector() # instanciate

for idx, fname in enumerate(fname_list[1:]):
    print(f'Processing image {idx+1}/{len(fname_list)}: {fname}')
    img_np = np.asarray(Image.open(path_images + fname))

    masks = signdetector(img_np) # run model
    img_np_focus = transform.multiply_rgb_image_by_binary_mask(img_np, masks>0)

    fig, axes = plt.subplots(2, 2)
    axes[0,0].imshow(img_np)
    axes[0,1].imshow(masks)
    axes[1,0].imshow(img_np_focus)

    fname_no_ext = os.path.splitext(fname)[0]
    fig.set_figheight(30)
    fig.set_figwidth(30)
    fig.tight_layout()
    fig.savefig(path_output + fname_no_ext + '.png')

    plt.close(fig)