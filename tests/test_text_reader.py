import unittest
from signreader.engine.text import TextReader
from PIL import Image

class TestTextReader(unittest.TestCase):
    def setUp(self):
        #self.img = Image.open('/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_3.png')
        self.img = Image.open('images/isolate_3.png')
        self.treader = TextReader()

    def test_call(self):
        scontent = self.treader(self.img)

if __name__ == '__main__':
    unittest.main()