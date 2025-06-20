from signreader.detector import ImageReader
from PIL import Image
import signreader.utils.plot as plot
import signreader.utils.io as io
import os
import pickle
import matplotlib.pyplot as plt

#path_output = '/Users/manu/boulot/unit_solutions/predictions/cellpose_test_set/'
path_output = '/Users/manu/boulot/unit_solutions/predictions/image_reader/cellpose_test_set_beautiful_examples/'

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

path_img = '/Users/manu/boulot/unit_solutions/data/datasets/segmentation/cellpose/test/'
fname_list = [
    #'BS-61727004_4_cropped.jpg',  # done
    #'BS-61826902_1_cropped_part2.jpg',  # done
    #'BS-61727004_4_cropped.jpg',  # done
    #'BS-61826902_1_cropped_part1.jpg',  # done
    #'BS-61826902_1_cropped_part2.jpg',  # done
    #'OW-001079-01_1.jpg',  # done
    #'OW-031931-01_4.jpg',  # done
    #'OW-032642-01_6.jpg',  # done
    #'OW-032653-01_7.jpg',  # done
    'OW-034179-01_1.jpg',
]

ireader = ImageReader(print=True)

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
