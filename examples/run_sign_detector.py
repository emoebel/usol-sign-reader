from signreader.engine.sign import SignDetector
import signreader.utils.transform as transform
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Open image:
img_np = np.asarray(Image.open('/path/to/image.jpg'))

# Instanciate:
signdetector = SignDetector()

# Run:
masks = signdetector(img_np)

# Plot result:
img_np_focus = transform.multiply_rgb_image_by_binary_mask(img_np, masks>0)

fig, axes = plt.subplots(2, 2)
axes[0,0].imshow(img_np)
axes[0,1].imshow(masks)
axes[1,0].imshow(img_np_focus)

fig.set_figheight(30)
fig.set_figwidth(30)
fig.tight_layout()
fig.savefig('/path/to/result.png')