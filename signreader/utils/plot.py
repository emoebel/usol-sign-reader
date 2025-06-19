import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_bounding_boxes(ax, img_np, boxes, class_names):
    ax.imshow(img_np)
    ax.set_title('Detected signs and symbols')
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        label = class_names[class_id]

        # Ajouter une boîte rectangle
        width, height = x2 - x1, y2 - y1
        rect = patches.Rectangle(
            (x1, y1),
            width,
            height,
            linewidth=1,
            edgecolor='magenta',
            facecolor='none',
        )
        ax.add_patch(rect)

        # Ajouter le texte (label + score)
        text = f"{label} {confidence:.2f}"
        ax.text(
            x1,
            y1 - 5,
            text,
            color='magenta',
            fontsize='medium',
        )


def plot_text_lines(ax, img_np, icontent):
    ax.imshow(img_np)
    ax.set_title('Detected text lines')
    for scontent in icontent: # for each sign in image
        for lcontent in scontent: # for each line in sign

            ax.plot(
                (lcontent['pos_dest'][0], lcontent['pos_dura'][0]),
                (lcontent['pos_dest'][1], lcontent['pos_dura'][1]),
                color='magenta',
            )


def plot_detector_result(img_np, masks, boxes, class_names, icontent):
    mask_binary = masks >= 1

    # Multiply image by mask, so we see only signs. Everything else is blacked out
    img_np_focus = np.zeros(img_np.shape, dtype=np.uint8)
    for channel in range(3):
        img_np_focus[:, :, channel] = img_np[:, :, channel] * mask_binary

    fig, axes = plt.subplots(1,3)
    axes[0].imshow(img_np)
    axes[0].set_title('Input image')

    plot_bounding_boxes(axes[1], img_np_focus, boxes, class_names)
    plot_text_lines(axes[2], img_np_focus, icontent)

    fig.set_figheight(15)
    fig.set_figwidth(45)
    fig.tight_layout()

    return fig, axes