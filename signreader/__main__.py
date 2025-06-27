import argparse
import os
import pickle
from signreader.detector import ImageReader
import signreader.utils.io as io
import signreader.utils.plot as plot
import matplotlib.pyplot as plt
from PIL import Image


def main():
    # Define arguments:
    parser = argparse.ArgumentParser(description='Segment a tomogram.')
    parser.add_argument('-models', action='store', dest='path_models', help='path to AI models')
    parser.add_argument('-image', action='store', dest='path_image', help='path to input image')
    parser.add_argument('-out', action='store', dest='path_out', help='path to output folder')
    args = parser.parse_args()

    ireader = ImageReader(print_flag=True)
    img_pil = Image.open(args.path_image)
    icontent = ireader(img_pil)

    img_np, masks, boxes, class_names, _ = ireader.get_data()
    fig, axes = plot.plot_detector_result(img_np, masks, boxes, class_names, icontent)
    plt.close(fig)

    fname = os.path.basename(args.path_image)
    fname_no_ext = os.path.splitext(fname)[0]
    # Save result plot:
    fig.savefig(os.path.join(args.path_out, fname_no_ext + '.png'))
    # Save result txt:
    #io.save_image_content_as_txt(icontent, os.path.join(args.path_out, fname_no_ext + '.txt'))
    # Save result csv:
    io.save_image_content_as_csv(icontent, class_names, os.path.join(args.path_out, fname_no_ext + '.csv'))
    # Save result pickle:
    with open(os.path.join(args.path_out, fname_no_ext + '.pkl'), "wb") as f:
        pickle.dump(icontent, f)


if __name__ == "__main__":
    main()