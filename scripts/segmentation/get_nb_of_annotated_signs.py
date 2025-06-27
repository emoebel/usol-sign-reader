import pandas as pd
import signreader.utils.io as io

path = '/Users/manu/boulot/unit_solutions/data/annotations/segmentation/napari_polygons/'

fname_list = io.get_fname_list_from_dir(path, ext='csv')

n_signs = 0
for fname in fname_list:
    print(fname)
    df = pd.read_csv(path + fname + '.csv')
    polygon_idx_list = list(set(df['index']))
    n_signs += len(polygon_idx_list)

print(f'Number of signs: {n_signs}')