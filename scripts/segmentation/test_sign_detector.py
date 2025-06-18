from cellpose import models, plot
import matplotlib.pyplot as plt
import utils.io as io
import time

class SignDetector:
    def __init__(self):
        self.model = models.CellposeModel(pretrained_model='/Users/manu/boulot/unit_solutions/training/cellpose/v1/round4/model_cellpose_e30-40')

    def __call__(self, img):
        '''

        :param img: (numpy array) of shape (Height, Width, Channel=3), and with dtype=uint8
        :return: (numpy array) of shape (Height, Width), and with dtype=uint16. Contains the segmentation map
        '''
        return self.model.eval(img, batch_size=1)[0]

# Load your image
img = io.open_img_as_np_array('/Users/manu/boulot/unit_solutions/data/datasets/segmentation/cellpose/test/48173-1_2.jpg')

# Instanciate
sdetector = SignDetector()

# Launch processing
start = time.time()
masks = sdetector(img)
end = time.time()
print('Processing time: ' + str(end-start) + ' seconds')  # This just was 55secs

# Plot result
fig, axes = plt.subplots(1,2)
axes[0].imshow(img)
axes[1].imshow(masks)
fig.savefig('testset_mask.png')

#model = models.CellposeModel(pretrained_model='/Users/manu/boulot/unit_solutions/training/cellpose/v1/round4/model_cellpose_e30-40')

#img = io.open_img_as_np_array('/Users/manu/boulot/unit_solutions/data/datasets/bbox/yolo/images/val/124786-1_1.jpg')

#flow_threshold = 0.4
#cellprob_threshold = 0.0
#tile_norm_blocksize = 0

#masks, flows, styles = model.eval(
#    img,
#    batch_size=1,
#    flow_threshold=flow_threshold,
#    cellprob_threshold=cellprob_threshold,
#    normalize={"tile_norm_blocksize": tile_norm_blocksize}
#)  # on cpu, this just took ~20min to run

#fig = plt.figure(figsize=(12,5))
#plot.show_segmentation(fig, img, masks, flows[0])
#plt.tight_layout()
#plt.show()

#plt.imsave('testset_mask.png', masks)  # for visu