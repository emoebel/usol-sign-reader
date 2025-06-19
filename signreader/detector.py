from signreader.engine.text import TextReader
from signreader.engine.sign import SignDetector
from signreader.engine.symbol import SymbolDetector
import signreader.utils.analysis as analysis

import numpy as np
from PIL import Image

class ImageReader:
    def __init__(self, print=False, plot=False):
        # Running params:
        self.print = print
        self.plot = plot

        # Engines:
        self.textreader = TextReader()
        self.signdetector = SignDetector()
        self.symbdetector = SymbolDetector()

        # Data:
        self.img_np = None
        self.masks = None
        self.icontent = None
        self.boxes = None

    def __call__(self, img_pil):
        '''
        This is the function that calls the whole pipeline.

        :param img_pil: (PIL.Image) input image
        :return: (list) image content with all detected information

        Image content object looks like:
        icontent[idx_sign][idx_line] = {
            'destination': ' Diessenhofen',
            'duration': ' 2h 10min',
            'pos_dest': (418.2041015625, 267.0),
            'pos_dura': (572.279296875, 274.0),
            'symbols': [1, 2], }
        '''
        self.initialize_data()

        img_np = np.asarray(img_pil)

        # First, get instance masks
        if self.print: print('[IR] Running sign detector...')
        masks = self.signdetector(img_np)
        idx_instance_list = np.unique(masks)[1:] # this gives the instance idx of each sign

        icontent = [] # instanciate image content object
        for idx_instance in idx_instance_list: # for each sign
            if self.print: print(f'[IR] Analyzing sign {idx_instance}...')
            mask_sign = masks == idx_instance # get mask specific to current sign

            # Multiply image by mask, and get and image focused on current sign. Everything else is blacked out
            img_np_focus = np.zeros(img_np.shape, dtype=np.uint8)
            for channel in range(3):
                img_np_focus[:, :, channel] = img_np[:, :, channel] * mask_sign

            img_pil_focus = Image.fromarray(img_np_focus, 'RGB')

            # Read the text on sign:
            if self.print: print('[IR] Running text reader...')
            scontent = self.textreader(img_pil_focus)

            # Now, detect objects:
            if self.print: print('[IR] Running symbol detector...')
            boxes, class_names = self.symbdetector(img_np_focus) # TODO: in future version, detect on whole image so only called once

            # Now that we have detected everything that we need, we have to put these detections in relation
            # What symbol is part of which text line?
            if self.print: print('[IR] Putting all sign information together...')
            idx_closest_line_per_box = analysis.get_lines_for_boxes(boxes=boxes, scontent=scontent)

            for idx_line, lcontent in enumerate(scontent):  # for each line in sign
                idx_boxes = np.nonzero(np.array(idx_closest_line_per_box) == idx_line)[0]  # [0] because outputs a tupple

                class_lbl_list = None  # default value
                if len(idx_boxes) > 0:  # if for current line corresponding boxes have been found
                    class_lbl_list = []
                    for idx_box in idx_boxes:
                        box = boxes[idx_box]
                        class_lbl_list.append(int(box.cls[0]))

                lcontent['symbols'] = class_lbl_list
                scontent[idx_line] = lcontent

        icontent.append(scontent)
        self.set_data(img_np, masks, icontent)

        return icontent

    def initialize_data(self):
        self.img_np = None
        self.masks = None
        self.icontent = None

    def set_data(self, img_np, masks, icontent):
        self.img_np = img_np
        self.masks = masks
        self.icontent = icontent

    def get_data(self):
        return self.img_np, self.masks, self.icontent