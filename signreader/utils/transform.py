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


def multiply_rgb_image_by_binary_mask(img_np, mask):
    '''
    :param img_np: (numpy array) of size [H, W, C]
    :param mask: (numpy array) binary mask of size [H, W]
    :return:
    '''
    img_np_focus = np.zeros(img_np.shape, dtype=np.uint8)
    for channel in range(3):
        img_np_focus[:, :, channel] = img_np[:, :, channel] * mask
    return img_np_focus


def get_scontent_without_none_coordinates(scontent):
    '''
    Sometimes TextReader makes errors and does not detect text lines correctly. In this case, text line coordinates
    lcontent['pos_dest'] or lcontent['pos_dura'] can be (None, None), which produce errors later on when using
    utils.transform.distance_btw_point_and_line. Therefor I make an approximation: the missing coordinate (pos_dest
    or pos_dura) is replaced by the existing one (pos_dura or pos_dest), but shifted horizontally. I hope that there are
    no cases where both coordinates are missing.
    :param scontent:
    :return:
    '''
    offset = 30 # in pixels
    for idx, lcontent in enumerate(scontent):
        if lcontent['pos_dest'] == (None, None) and lcontent['pos_dura'] == (None, None):
            print(f'/!\ In line {idx}, both pos_dest and pos_dura are None')

        if lcontent['pos_dest'] == (None, None):
            [x, y] = lcontent['pos_dura']
            lcontent['pos_dest'] = (x - offset, y)  # shifted left
        if lcontent['pos_dura'] == (None, None):
            [x, y] = lcontent['pos_dest']
            lcontent['pos_dura'] = (x + offset, y)  # shifted right

        scontent[idx] = lcontent

    return scontent


def get_scale_factor_max_image_size(img_np, max_img_size):
    img_shape = img_np.shape[:2]

    idx_ax_small = int(np.argmin(img_shape))
    idx_ax_large = int(np.argmax(img_shape))

    l_small = img_shape[idx_ax_small]
    l_large = img_shape[idx_ax_large]

    scale_factor = max_img_size / l_large
    return scale_factor


def get_scale_factor_min_image_size(img_np, min_img_size):
    img_shape = img_np.shape[:2]

    idx_ax_small = int(np.argmin(img_shape))
    idx_ax_large = int(np.argmax(img_shape))

    l_small = img_shape[idx_ax_small]
    l_large = img_shape[idx_ax_large]

    scale_factor = min_img_size / l_small
    return scale_factor


def resize_img_with_scale_factor(img_np, scale_factor):
    img_shape = img_np.shape[:2]

    img_shape_new = [
        int(np.round(img_shape[0] * scale_factor)),
        int(np.round(img_shape[1] * scale_factor)),
    ]

    img_new = skimage.transform.resize(
        image=img_np,
        output_shape=img_shape_new,
        preserve_range=True,
    )
    img_new = img_new.astype(np.uint8)

    return img_new