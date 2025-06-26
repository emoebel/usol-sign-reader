from ultralytics import YOLO

class SymbolDetector:
    def __init__(self, path_model=None):
        if path_model is None:
            path_model = '/Users/manu/boulot/unit_solutions/training/yolo/unitsol_symbols_v0/run4/weights/last.pt'
        self.model = YOLO(path_model)

    def __call__(self, img):
        '''

        :param img: (numpy array) of shape (Height, Width, Channel=3), and with dtype=uint8
        :return: (ultralytics.engine.results.Boxes) detected boxes and associated classes. Also outputs a (dict) mapping class indices to class names.
        '''
        result = self.model(img)[0]
        return result.boxes, result.names