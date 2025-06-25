from signreader.engine.symbol import SymbolDetector
import signreader.utils.plot as plot
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Open image:
img_np = np.asarray(Image.open('/path/to/image.jpg'))

# Instanciate:
symbdetector = SymbolDetector()

# Run:
boxes, class_names = symbdetector(img_np)

# Plot result:
fig, ax = plt.subplots(1, 1)
plot.plot_bounding_boxes(ax, img_np, boxes, class_names)

fig.set_figheight(15)
fig.set_figwidth(15)
fig.tight_layout()
fig.savefig('/path/to/result.png')