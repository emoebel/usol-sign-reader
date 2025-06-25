from signreader.detector import ImageReader
from PIL import Image
import signreader.utils.plot as plot
import signreader.utils.io as io
import os
import pickle
import matplotlib.pyplot as plt

#path_output = '/Users/manu/boulot/unit_solutions/predictions/cellpose_test_set/'
#path_output = '/Users/manu/boulot/unit_solutions/predictions/image_reader/cellpose_test_set_beautiful_examples/'
#path_output = '/Users/manu/boulot/unit_solutions/predictions/image_reader/yolo_test_set_beautiful_examples/'
path_output = '/Users/manu/boulot/unit_solutions/predictions/image_reader/tmp/'

# path_img = '/Users/manu/boulot/unit_solutions/data/datasets/segmentation/cellpose/test/'
# fname_list = [
#     #'48159-1_2.jpg', # done
#     #'48618-1_2.jpg', # done
#     #'48930-1_1.jpg', # done
#     #'91712-1_1.jpg', # done
#     '118098-1_3.jpg',
#     '125146-2_2.jpg',
#     '125279-1_1.jpg',
#     '125321-1_4.jpg',
#     '126077-1_3.jpg',
#     '126518-1_3.jpg',
#     '139547-1_2.jpg',
#     'LIE-16402002_4.jpg',
#     'OW-001079-01_1.jpg',
#     'OW-003877-01_2.jpg',
#     'OW-004099-01_5.jpg',
#     'OW-004338-01_6.jpg',
#     'OW-005025-01_3.jpg',
#     'OW-005217-01_5.jpg',
#     'OW-005411-02_1.jpg',
#     'OW-032642-01_6.jpg',
# ]

# path_img = '/Users/manu/boulot/unit_solutions/data/datasets/segmentation/cellpose/test/'
# fname_list = [
#     #'BS-61727004_4_cropped.jpg',  # done
#     #'BS-61826902_1_cropped_part2.jpg',  # done
#     #'BS-61727004_4_cropped.jpg',  # done
#     #'BS-61826902_1_cropped_part1.jpg',  # done
#     #'BS-61826902_1_cropped_part2.jpg',  # done
#     #'OW-001079-01_1.jpg',  # done
#     #'OW-031931-01_4.jpg',  # done
#     #'OW-032642-01_6.jpg',  # done
#     #'OW-032653-01_7.jpg',  # done
#     'OW-034179-01_1.jpg',
# ]
path_img = '/Users/manu/boulot/unit_solutions/data/datasets/bbox/yolo/images/val/'
fname_list = [
    #'OW-004338-01_6.jpeg',  # done
    #'OW-005411-02_1.jpeg',
    #'OW-032652-01_5.jpg',
    #'OW-034179-01_1.jpg',
    #'OW-035757-01_7.jpeg',
    #'OW-035768-01_3.jpeg',
    #'OW-035770-01_2.jpeg',  # one of detected instances is too small (segmentation error) and results in TextReader error
    #'OW-035802-01_6.jpeg',
    #'OW-035803-01_4.jpeg',
    #'OW-035836-01_5.jpeg',
    #'OW-035944-01_5.jpeg',
    #'OW-038659-01_4.jpg',
    #'SZ-67521506_1.jpg',
    #'121875-1_1.jpeg',
    #'124786-1_1.jpg',
    #'126461-1_1.jpg',
    #'BL-61526301_1.jpg',
    #'BL-61926307_3.jpg',
    #'OW-035688-01_1.jpg',
    #'OW-035691-01_7.jpg',
    #'OW-035700-01_5.jpg',
    #'OW-035720-01_4.jpg',
    #'OW-039020-01_1.jpg',
    #'TG-32-603_1.jpg',
    'TG-53-301_1.jpg',
    #'TG-53-303_1.jpg',
]


ireader = ImageReader(print_flag=True)

for idx, fname in enumerate(fname_list):
    print(f'Processing image {idx+1}/{len(fname_list)}: {fname}')

    img_pil = Image.open(path_img + fname)

    icontent = ireader(img_pil)

    img_np, masks, boxes, class_names, _ = ireader.get_data()
    fig, axes = plot.plot_detector_result(img_np, masks, boxes, class_names, icontent)
    plt.close(fig)

    fname_no_ext = os.path.splitext(fname)[0]
    # Save result plot:
    fig.savefig(path_output + fname_no_ext + '.png')
    # Save result txt:
    io.save_image_content_as_txt(icontent, path_output + fname_no_ext + '.txt')
    # Save result pickle:
    with open(path_output + fname_no_ext + '.pkl', "wb") as f:
        pickle.dump(icontent, f)
