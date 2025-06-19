# Here I want to get a fname_list of files that are both (i) been annotated (i.e. present in annot json file) and
# (ii) present in class folder (as existing in original data set). This will help me to select a test set.

import signreader.utils.io as io
import numpy as np


# path_class_folder = '/Users/manu/boulot/unit_solutions/data/images/45_Strassenbahn/'
# path_output = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_strassenbahn.txt'
# n = 10  # nb of images randomly selected for test set
# path_class_folder = '/Users/manu/boulot/unit_solutions/data/images/9_Sessellift/'
# path_output = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_sessellift.txt'
# n = 12  # nb of images randomly selected for test set
# path_class_folder = '/Users/manu/boulot/unit_solutions/data/images/5_Schiffstation/'
# path_output = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_schiffstation.txt'
# n = 12  # nb of images randomly selected for test set
# path_class_folder = '/Users/manu/boulot/unit_solutions/data/images/48_Feuerstelle/'
# path_output = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_feuerstelle.txt'
# n = 17  # nb of images randomly selected for test set
# path_class_folder = '/Users/manu/boulot/unit_solutions/data/images/6_Zahnrad/'
# path_output = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_zahnrad.txt'
# n = 10  # nb of images randomly selected for test set
path_class_folder = '/Users/manu/boulot/unit_solutions/data/images/8_Gondelbahn/'
path_output = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset_gondelbahn.txt'
n = 5  # nb of images randomly selected for test set

fname_list_class = io.get_fname_list_from_dir(path_class_folder, 'jpg') + \
                   io.get_fname_list_from_dir(path_class_folder, 'jpeg') + \
                   io.get_fname_list_from_dir(path_class_folder, 'png')

path_annot_file = '/Users/manu/Downloads/project-3-at-2025-06-12-09-00-c3c15364.json'

fname_list_annotated = io.get_fnames_from_lstudio_json(path_annot_file)



fname_list_new = list( set(fname_list_annotated).intersection(fname_list_class) )

#random.shuffle(fname_list_new)  # we want to choose n images randomly
fname_list_new = list(np.random.permutation(fname_list_new))

io.save_fname_list_to_txt(fname_list_new[:n], path_output)
