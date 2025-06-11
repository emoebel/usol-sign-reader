# Here I want to fine-tune the img selection to annotate. I can't annotate everything due to time constraints,
# so I have to select fewer images in a smart manner. I want to select images of rare classes, but only if they have
# not been already annotated.

import utils.io as io

path_annot_file = '/Users/manu/Downloads/project-3-at-2025-06-10-10-31-644aa820.json'

fname_list_annotated = io.get_fnames_from_lstudio_json(path_annot_file)

path_strassenbahn = '/Users/manu/boulot/unit_solutions/data/images/45_Strassenbahn/'
fname_list_strassenbahn = io.get_fname_list_from_dir(path_strassenbahn, 'jpg') + \
    io.get_fname_list_from_dir(path_strassenbahn, 'jpeg') + \
    io.get_fname_list_from_dir(path_strassenbahn, 'png')

fname_list_new = list(set(fname_list_strassenbahn) - set(fname_list_annotated))

for fname in fname_list_strassenbahn:
    if fname in fname_list_annotated: print(fname + ' has already been annotated.')