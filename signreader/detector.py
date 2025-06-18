from signreader.engine.text import TextReader
from signreader.engine.sign import SignDetector
from signreader.engine.symbol import SymbolDetector

class ImageReader:
    def __init__(self):
        self.textreader = TextReader()
        self.signdetector = SignDetector()
        self.symbdetector = SymbolDetector()