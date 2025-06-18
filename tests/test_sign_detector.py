import unittest
from signreader.engine.sign import SignDetector
from PIL import Image
import numpy as np

class TestSignDetector(unittest.TestCase):
    def setUp(self):
        self.img = np.asarray(Image.open('/Users/manu/boulot/unit_solutions/data/datasets/segmentation/cellpose/test/48173-1_2.jpg'))
        self.signdetector = SignDetector()

    def test_call(self):
        masks = self.signdetector(self.img) # takes ~55secs on i7 CPU

if __name__ == '__main__':
    unittest.main()