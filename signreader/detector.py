from signreader.engine.text import TextReader
from signreader.engine.sign import SignDetector
from signreader.engine.symbol import SymbolDetector
import signreader.utils.analysis as analysis
import signreader.utils.transform as transform

import os
import numpy as np
from PIL import Image

class ImageReader:
    def __init__(self, path_models=None, print_flag=False):
        # Get model paths:
        if path_models is None:
            path_models = '/Users/manu/boulot/unit_solutions/training/models/'
        fname_cellpose, fname_yolo = self.get_model_paths_from_folder(path_models)

        # Running params:
        self.print = print_flag

        # Engines:
        self.textreader = TextReader(print_flag=print_flag)
        self.signdetector = SignDetector(path_model=fname_cellpose)
        self.symbdetector = SymbolDetector(path_model=fname_yolo)

        # Data:
        self.img_np = None
        self.masks = None
        self.boxes = None
        self.class_names = None
        self.icontent = None

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
        if self.print: print('[ImageReader] Running sign detector...')
        masks = self.signdetector(img_np)
        idx_instance_list = np.unique(masks)[1:] # this gives the instance idx of each sign

        # Next, detect objects:
        if self.print: print('[ImageReader] Running symbol detector...')
        boxes, class_names = self.symbdetector(img_np)

        icontent = [] # instanciate image content object
        for idx_instance in idx_instance_list: # for each sign
            if self.print: print(f'[ImageReader] Analyzing sign {idx_instance}...')
            mask_sign = masks == idx_instance # get mask specific to current sign

            # Use the mask to get keep only boxes that are part of mask
            box_list_in_mask = analysis.which_boxes_are_in_mask(boxes, mask_sign)

            # Multiply image by mask, and get and image focused on current sign. Everything else is blacked out
            img_np_focus = transform.multiply_rgb_image_by_binary_mask(img_np, mask_sign)
            img_pil_focus = Image.fromarray(img_np_focus, 'RGB')

            # Read the text on sign:
            if self.print: print('[ImageReader] Running text reader...')
            scontent = self.textreader(img_pil_focus)

            # Now that we have detected everything that we need, we have to put these detections in relation
            # What symbol is part of which text line?
            # TODO: rest of this block could be self.put_detections_in_relation()
            if self.print: print('[ImageReader] Putting all sign information together...')
            scontent = self.put_symbols_and_text_in_relation(scontent, box_list_in_mask)
            # scontent = transform.get_scontent_without_none_coordinates(scontent) # see function description for explanation
            # idx_closest_line_per_box = analysis.get_lines_for_boxes(boxes=box_list_in_mask, scontent=scontent)
            #
            # for idx_line, lcontent in enumerate(scontent):  # for each line in sign
            #     idx_boxes = np.nonzero(np.array(idx_closest_line_per_box) == idx_line)[0]  # [0] because outputs a tupple
            #
            #     class_lbl_list = None  # default value
            #     if len(idx_boxes) > 0:  # if for current line corresponding boxes have been found
            #         class_lbl_list = []
            #         for idx_box in idx_boxes:
            #             box = box_list_in_mask[idx_box]
            #             class_lbl_list.append(int(box.cls[0]))
            #
            #     lcontent['symbols'] = class_lbl_list
            #     scontent[idx_line] = lcontent

            icontent.append(scontent)

        self.set_data(img_np, masks, boxes, class_names, icontent)

        return icontent

    def put_symbols_and_text_in_relation(self, scontent, box_list):
        '''
        This functions analyses detected text and detected symbols (boxes), and establishes their relation.
        To which text line corresponds which box?
        :param scontent: (list of dict)
        :return: (list of dict)
        '''
        scontent = transform.get_scontent_without_none_coordinates(scontent)  # see function description for explanation
        idx_closest_line_per_box = analysis.get_lines_for_boxes(boxes=box_list, scontent=scontent)

        for idx_line, lcontent in enumerate(scontent):  # for each line in sign
            idx_boxes = np.nonzero(np.array(idx_closest_line_per_box) == idx_line)[0]  # [0] because outputs a tupple

            class_lbl_list = None  # default value
            if len(idx_boxes) > 0:  # if for current line corresponding boxes have been found
                class_lbl_list = []
                for idx_box in idx_boxes:
                    box = box_list[idx_box]
                    class_lbl_list.append(int(box.cls[0]))

            lcontent['symbols'] = class_lbl_list
            scontent[idx_line] = lcontent
        return scontent

    def initialize_data(self):
        self.img_np = None
        self.masks = None
        self.boxes = None
        self.class_names = None
        self.icontent = None

    def set_data(self, img_np, masks, boxes, class_names, icontent):
        self.img_np = img_np
        self.masks = masks
        self.boxes = boxes
        self.class_names = class_names
        self.icontent = icontent

    def get_data(self):
        return self.img_np, self.masks, self.boxes, self.class_names, self.icontent

    def get_model_paths_from_folder(self, path_models):
        dir_fnames_yolo = os.listdir(os.path.join(path_models, 'yolo'))
        if len(dir_fnames_yolo) > 1:
            print('[ImageReader] Model loader error: yolo folder should contain only 1 file')

        fname_yolo = os.path.join(path_models, 'yolo', dir_fnames_yolo[0])

        dir_fnames_cellpose = os.listdir(os.path.join(path_models, 'cellpose'))
        if len(dir_fnames_cellpose) > 1:
            print('[ImageReader] Model loader error: cellpose folder should contain only 1 file')
        fname_cellpose = os.path.join(path_models, 'cellpose', dir_fnames_cellpose[0])

        return fname_cellpose, fname_yolo
