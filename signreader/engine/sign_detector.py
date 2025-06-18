from cellpose import models

class SignDetector:
    def __init__(self):
        self.model = models.CellposeModel(pretrained_model='/Users/manu/boulot/unit_solutions/training/cellpose/v1/round4/model_cellpose_e30-40')

    def __call__(self, img):
        '''

        :param img: (numpy array) of shape (Height, Width, Channel=3), and with dtype=uint8
        :return: (numpy array) of shape (Height, Width), and with dtype=uint16. Contains the segmentation map
        '''
        return self.model.eval(img, batch_size=1)[0]