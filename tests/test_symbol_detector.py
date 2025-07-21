import unittest
from signreader.engine.symbol import SymbolDetector
from PIL import Image
import numpy as np

class TestSymbolDetector(unittest.TestCase):
    def setUp(self):
        #self.img = np.asarray(Image.open('/Users/manu/boulot/unit_solutions/data/datasets/bbox/yolo/images/val/OW-004338-01_6.jpeg'))
        self.img = np.asarray(Image.open('images/OW-004338-01_6.jpeg'))
        self.symbdetector = SymbolDetector()

    def test_call(self):
        boxes = self.symbdetector(self.img) # takes ~3.5secs on i7 CPU

if __name__ == '__main__':
    unittest.main()