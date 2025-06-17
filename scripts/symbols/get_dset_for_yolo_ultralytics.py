import os
import utils.io as io
import shutil

def get_fname_list_with_ext_from_dir(dir_path, ext='csv'):
    # Get all files in directory:
    dir_fnames = os.listdir(dir_path)
    fname_list = []
    for fname in dir_fnames:
        if fname[0] != '.' and os.path.splitext(fname)[1] == '.' + ext:
            fname_list.append(fname)
    fname_list.sort()

    return fname_list


path_in = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/project-3-at-2025-06-16-09-04-d5595fd4/'
path_out = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/yolo/'

# fname_list_subset = io.open_fname_list_from_txt('/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_testset.txt')
# subset = 'val/'
fname_list_subset = io.open_fname_list_from_txt('/Users/manu/boulot/unit_solutions/data/datasets/bbox/fname_list_trainset.txt')
subset = 'train/'

# Get the fname list of images in dset export by lstudio
path_dset_lstudio_img = path_in + 'images/'
fname_list_lstudio = get_fname_list_with_ext_from_dir(path_dset_lstudio_img, 'jpg') + \
    get_fname_list_with_ext_from_dir(path_dset_lstudio_img, 'jpeg') + \
    get_fname_list_with_ext_from_dir(path_dset_lstudio_img, 'png')

# Lstudio has renamed the files with a prefix
fname_list_all = []
for fname in fname_list_lstudio:
    fname_new = '-'.join(fname.split('-')[1:])  # we want 'b9c1c77f-OW-031931-01_4.jpeg' -> 'OW-031931-01_4.jpeg'
    fname_new = os.path.splitext(fname_new)[0]
    fname_list_all.append( fname_new )


for idx, fname in enumerate(fname_list_subset):
    print(fname)
    fname_lstudio = fname_list_lstudio[fname_list_all.index(fname)]  # get corresponding lstudio fname

    fname_lstudio_img = fname_lstudio
    fname_lstudio_lbl = os.path.splitext(fname_lstudio)[0] + '.txt'

    img_ext = os.path.splitext(fname_lstudio_img)[1]

    # Copy img:
    shutil.copyfile(
        src=path_in + 'images/' + fname_lstudio_img,
        dst=path_out + 'images/' + subset + fname + img_ext,
    )

    # Copy lbl:
    shutil.copyfile(
        src=path_in + 'labels/' + fname_lstudio_lbl,
        dst=path_out + 'labels/' + subset + fname + '.txt',
    )
