import numpy as np
import skimage

def normalize_image_size(img, lmap, min_size=512):
    '''
    Resizes smallest image axe to min_size, by keeping aspect ratio. Applies transform to both image and label map.
    :param img: numpy array
    :param lmap: numpy array
    :param min_size:
    :return: [numpy array, numpy array] transformed image and label map
    '''
    img_shape = img.shape[:2]

    idx_ax_small = int(np.argmin(img_shape))
    idx_ax_large = int(np.argmax(img_shape))

    l_small = img_shape[idx_ax_small]
    l_large = img_shape[idx_ax_large]

    min_size = 512

    l_small_new = min_size
    l_large_new = int(np.round((l_large * min_size) / l_small))

    img_shape_new = [None, None]

    if idx_ax_small==idx_ax_large:  # this happens when img is squared (lenght = height)
        idx_ax_small = 0
        idx_ax_large = 1

    img_shape_new[idx_ax_small] = l_small_new
    img_shape_new[idx_ax_large] = l_large_new

    img_new = skimage.transform.resize(
        image=img,
        output_shape=img_shape_new,
        preserve_range=True,
    )
    # img_new = (img_new*255).astype(np.uint8)
    img_new = img_new.astype(np.uint8)

    lmap_new = skimage.transform.resize(
        image=lmap,
        output_shape=img_shape_new,
        preserve_range=True,
        order=0,  # for label map we have to use nearest-neighbor interpolation (default is 1: Bilinear)
    )

    return img_new, lmap_new