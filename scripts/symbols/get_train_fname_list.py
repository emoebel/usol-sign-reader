import os
import utils.io as io


path_out = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/'

fname_list_test = io.open_fname_list_from_txt('/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset.txt')

path_dset_lstudio = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/project-3-at-2025-06-16-09-04-d5595fd4/images/'
fname_list_lstudio = io.get_fname_list_from_dir(path_dset_lstudio, 'jpg') + \
    io.get_fname_list_from_dir(path_dset_lstudio, 'jpeg') + \
    io.get_fname_list_from_dir(path_dset_lstudio, 'png')


fname_list = []
for fname in fname_list_lstudio:
    fname_new = '-'.join(fname.split('-')[1:])  # we want 'b9c1c77f-OW-031931-01_4.jpeg' -> 'OW-031931-01_4.jpeg'
    fname_list.append( fname_new )

fname_list_train = list(set(fname_list) - set(fname_list_test))

io.save_fname_list_to_txt(fname_list_train, path_out+'fname_list_trainset.txt')