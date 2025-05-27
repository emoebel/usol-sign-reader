import utils.io as io
import napari.layers
import numpy as np

path_polygons = '/Users/manu/boulot/unit_solutions/annotations/segmentation/napari_polygons/'
path_images = '/Users/manu/boulot/unit_solutions/data/all/'
path_output = '/Users/manu/boulot/unit_solutions/annotations/segmentation/segmentation_maps/'


fname_list = io.get_fname_list_from_dir(path_polygons)

fname = fname_list[0]

path_csv_file = path_polygons + fname + '.csv'

# # Prepare data argument for napari.layers.Shapes construcotr
# df = pd.read_csv(path_csv_file)
#
# polygon_idx_list = list(set(df['index']))
# polygon_list = []
# for polygon_idx in polygon_idx_list:
#     df_polygon = df.loc[df['index']==polygon_idx]
#     polygon_vertex_coord_list = []
#     for idx, row in df_polygon.iterrows():
#         polygon_vertex_coord_list.append([row['axis-0'], row['axis-1']])
#
#     polygon_list.append(polygon_vertex_coord_list)

data = io.get_data_for_shapes_layer_from_polygon_csv(path_csv_file)

# Create Shapes object:
shapes_layer = napari.layers.Shapes(
    data=data,
    shape_type='polygon',
)


# from napari_builtins.io import read_csv
# data, column_names, layer_type = read_csv(path_csv_file)
#
# # Create Shapes object:
# shapes_layer = napari.layers.Shapes(
#     data=data,
#     shape_type='polygon',
# )

# Get image shape for Shapes.to_labels:
# from PIL import Image
# def open_img_as_np_array(fname):
#     return np.asarray(Image.open(fname))

img = io.open_img_as_np_array(path_images + fname + '.jpg')
img_shape = img.shape[:2]

# Get segmentation map from Shapes object:
seg_map = shapes_layer.to_labels(
    labels_shape=img_shape,
)
# seg_map.shape
# np.unique(seg_map)
#
# seg_map = shapes_layer.to_masks(
#     mask_shape=img_shape,
# )
# seg_map.shape
# np.unique(seg_map)



# data = [
#     [[50.2, 50], [50, 100], [100, 100], [100, 50], [80, 50]],
# ]
#
# # Create Shapes object:
# shapes_layer = napari.layers.Shapes(
#     data=data,
#     shape_type='polygon',
# )
#
# # Get segmentation map from Shapes object:
# seg_map = shapes_layer.to_labels(
#     labels_shape=[200, 200],
# )

import matplotlib.pyplot as plt
plt.imsave('seg_map.png', seg_map)  # for visu