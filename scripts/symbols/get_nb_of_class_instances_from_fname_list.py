# This scripts helps to constitute the test set. We want this set to contain (i) beautiful examples for presentations
# (for example clean images with lots of different symbols) and (ii) around 20 instances per class.

import utils.io as io
import pandas as pd
import os

fname_list = io.open_fname_list_from_txt('/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_beautiful_examples.txt') + \
    io.open_fname_list_from_txt('/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_strassenbahn.txt') + \
    io.open_fname_list_from_txt('/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_sessellift.txt') + \
    io.open_fname_list_from_txt('/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_schiffstation.txt') + \
    io.open_fname_list_from_txt('/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_feuerstelle.txt') + \
    io.open_fname_list_from_txt('/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_zahnrad.txt') + \
    io.open_fname_list_from_txt('/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_gondelbahn.txt')

# -> this is now our test set
io.save_fname_list_to_txt(fname_list, '/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset.txt')


path_annot_file = '/Users/manu/boulot/unit_solutions/data/annotations/bbox/lstudio/project-3-at-2025-06-16-12-29-cbcca54c.json'
df = pd.read_json(path_annot_file)

class_instance_nb = {
    'bahnhof': 0,
    'bushof': 0,
    'schiffstation': 0,
    'zahnrad-standseilbahn': 0,
    'luftseilbahn': 0,
    'gondelbahn': 0,
    'sessellift': 0,
    'strassenbahn': 0,
    'huette': 0,
    'restaurant': 0,
    'feuerstelle': 0,
    'aussichtspunkt': 0,
    'other': 0,
}


for fname in fname_list:
    fname = os.path.splitext(fname)[0]
    print(fname)
    for row in df.itertuples():
        fname_lstudio = row.file_upload
        fname_lstudio = '-'.join(fname_lstudio.split('-')[1:])
        fname_lstudio = os.path.splitext(fname_lstudio)[0]

        if fname == fname_lstudio:
            # Get nb of class instanes
            bbox_list = row.annotations[0]['result']
            for bbox in bbox_list:
                label = bbox['value']['rectanglelabels'][0]
                class_instance_nb[label] += 1

