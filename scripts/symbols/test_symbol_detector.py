from ultralytics import YOLO
import utils.io as io
import time

class SymbolDetector:
    def __init__(self):
        self.model = YOLO('/Users/manu/boulot/unit_solutions/training/yolo/unitsol_symbols_v0/run4/weights/last.pt')

    def __call__(self, img):
        '''

        :param img: (numpy array) of shape (Height, Width, Channel=3), and with dtype=uint8
        :return: (ultralytics.engine.results.Boxes) detected boxes and associated classes
        '''
        result = self.model(img)[0]
        return result.boxes


# Load image
img = io.open_img_as_np_array('/Users/manu/boulot/unit_solutions/data/datasets/bbox/yolo/images/val/OW-004338-01_6.jpeg')

# Instanciate
symbdetector = SymbolDetector()

# Launch processing
start = time.time()
boxes = symbdetector(img)
end = time.time()
print('Processing time: ' + str(end-start) + ' seconds')  # 3.5secs