import os.path
import pandas as pd
from PIL import Image
import numpy as np

def get_fname_list_from_dir(dir_path, ext='csv'):
    # Get all files in directory:
    dir_fnames = os.listdir(dir_path)
    fname_list = []
    for fname in dir_fnames:
        if fname[0] != '.' and os.path.splitext(fname)[1] == '.' + ext:
            fname_without_extension = os.path.splitext(fname)[0]
            fname_list.append(fname_without_extension)
    fname_list.sort()

    return fname_list


def save_fname_list_to_txt(my_list, filename):
    with open(filename, 'w') as file:
        for item in my_list:
            file.write(f"{item}\n")


def open_fname_list_from_txt(filename):
    with open(filename, 'r') as file:
        fname_list = []
        for line in file:
            fname_list.append(line[:-1])
    return fname_list


def get_data_for_shapes_layer_from_polygon_csv(fname_csv):
    """
    :param fname_csv: (str) file name of csv file, as created by saving Napari shapes layer
    :return data: (list) List of shape data, where each element is an (N, D) array of the N vertices of a shape in D dimensions. As needed by napari.layers.Shapes constructor.
    """
    df = pd.read_csv(fname_csv)

    polygon_idx_list = list(set(df['index']))
    data = []
    for polygon_idx in polygon_idx_list:
        df_polygon = df.loc[df['index'] == polygon_idx]
        polygon_vertex_coord_list = []
        for idx, row in df_polygon.iterrows():
            polygon_vertex_coord_list.append([row['axis-0'], row['axis-1']])

        data.append(polygon_vertex_coord_list)
    return data


def open_img_as_np_array(fname):
    return np.asarray(Image.open(fname))


def save_np_array_as_img(fname, array):
    pil_img = Image.fromarray(array)
    pil_img.save(fname)


def get_fnames_from_lstudio_json(path_annot_file):
    df = pd.read_json(path_annot_file)

    fname_list = []
    for row in df.itertuples():
        fname_lstudio = row.file_upload

        # lstudio adds an id in front of original fnale
        # we want 'b9c1c77f-OW-031931-01_4.jpeg' -> 'OW-031931-01_4.jpeg'
        fname = '-'.join(fname_lstudio.split('-')[1:])
        fname_list.append(fname)

    return fname_list