from signreader.detector import ImageReader
from PIL import Image
import signreader.utils.plot as plot
import signreader.utils.io as io
import pickle

# Open image:
img_pil = Image.open('/path/to/image.jpg')

# Instanciate:
ireader = ImageReader(print_flag=True)

# Run:
icontent = ireader(img_pil)

# Plot result:
img_np, masks, boxes, class_names, _ = ireader.get_data()
fig, axes = plot.plot_detector_result(img_np, masks, boxes, class_names, icontent)
fig.savefig('/path/to/result.png')

# Save result as txt:
io.save_image_content_as_txt(icontent, '/path/to/result.txt')

# Save result as pickle:
with open('/path/to/result.pkl', "wb") as f:
    pickle.dump(icontent, f)