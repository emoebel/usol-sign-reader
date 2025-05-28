from cellpose import io, models, train
io.logger_setup()

train_dir = '/Users/manu/boulot/unit_solutions/data/datasets/segmentation/cellpose_toy_dset/train/'
test_dir = '/Users/manu/boulot/unit_solutions/data/datasets/segmentation/cellpose_toy_dset/test/'

output = io.load_train_test_data(
    train_dir,
    test_dir,
    #image_filter=".tiff",
    mask_filter="_masks",
    look_one_level_down=False,
)
images, labels, image_names, test_images, test_labels, image_names_test = output

model = models.CellposeModel(gpu=False)

model_path, train_losses, test_losses = train.train_seg(
    model.net,
    train_data=images,
    train_labels=labels,
    test_data=test_images,
    test_labels=test_labels,
    weight_decay=0.1,
    learning_rate=1e-5,
    n_epochs=1,
    model_name="my_new_model",
)