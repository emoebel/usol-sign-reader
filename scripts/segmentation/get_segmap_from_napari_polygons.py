import utils.io as io
import napari.layers
import numpy as np

path_polygons = '/Users/manu/boulot/unit_solutions/annotations/segmentation/napari_polygons/'
path_images = '/Users/manu/boulot/unit_solutions/data/all/'
path_output = '/Users/manu/boulot/unit_solutions/annotations/segmentation/segmentation_maps/'


fname_list = io.get_fname_list_from_dir(path_polygons)

for fname in fname_list:
    print(fname)
    path_csv_file = path_polygons + fname + '.csv'
    data = io.get_data_for_shapes_layer_from_polygon_csv(path_csv_file)

    # Create Shapes object:
    shapes_layer = napari.layers.Shapes(
        data=data,
        shape_type='polygon',
    )

    # Get img shape:
    try:
        img = io.open_img_as_np_array(path_images + fname + '.jpg')
    except FileNotFoundError:
        img = io.open_img_as_np_array(path_images + fname + '.jpeg')
    img_shape = img.shape[:2]

    # Get segmentation map from Shapes object:
    seg_map = shapes_layer.to_labels(
        labels_shape=img_shape,
    )

    # Save seg_map:
    path_seg_map_file = path_output + fname + '.npy'
    np.save(path_seg_map_file, np.int8(seg_map))


# import matplotlib.pyplot as plt
# plt.imsave('seg_map.png', seg_map)  # for visu