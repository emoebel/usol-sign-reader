from cellpose import models
import signreader.utils.transform as transform
import skimage

class SignDetector:
    def __init__(self):
        self.model = models.CellposeModel(pretrained_model='/Users/manu/boulot/unit_solutions/training/cellpose/v1/round4/model_cellpose_e30-40')
        self.min_img_size = 512  # used as size norm for training
    def __call__(self, img_np):
        '''

        :param img: (numpy array) of shape (Height, Width, Channel=3), and with dtype=uint8
        :return: (numpy array) of shape (Height, Width), and with dtype=uint16. Contains the segmentation map
        '''
        # First, apply image size normalization (the same as used for training)
        scale_factor = transform.get_scale_factor_min_image_size(img_np, self.min_img_size)
        img_size_norm = transform.resize_img_with_scale_factor(img_np, scale_factor)

        # Then, predict:
        masks_size_norm = self.model.eval(img_size_norm, batch_size=1)[0]

        # Finally, apply inverse size norm to come back to orginial image size:
        masks = skimage.transform.resize(
            image=masks_size_norm,
            output_shape=img_np.shape[:2],
            preserve_range=True,
            order=0,  # for label map we have to use nearest-neighbor interpolation (default is 1: Bilinear)
        )
        return masks