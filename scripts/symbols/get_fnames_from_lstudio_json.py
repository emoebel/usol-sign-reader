import pandas as pd
import utils.io as io

path_annot_file = '/Users/manu/Downloads/project-3-at-2025-06-10-10-31-644aa820.json'

# def get_fnames_from_lstudio_json(path_annot_file):
#     df = pd.read_json(path_annot_file)
#
#     fname_list = []
#     for row in df.itertuples():
#         fname_lstudio = row.file_upload
#
#         # lstudio adds an id in front of original fnale
#         # we want 'b9c1c77f-OW-031931-01_4.jpeg' -> 'OW-031931-01_4.jpeg'
#         fname = '-'.join(fname_lstudio.split('-')[1:])
#         fname_list.append(fname)
#
#     return fname_list

fname_list = io.get_fnames_from_lstudio_json(path_annot_file)