import os.path

def get_fname_list_from_dir(dir_path, ext='csv'):
    # Get all files in directory:
    dir_fnames = os.listdir(dir_path)
    fname_list = []
    for fname in dir_fnames:
        if fname[0] != '.' and os.path.splitext(fname)[1] == '.' + ext:
            fname_list.append(fname)
    fname_list.sort()

    return fname_list
