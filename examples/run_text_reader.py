from signreader.engine.text import TextReader
from PIL import Image

# Open image:
# For the text reader to function correctly, all except the considered sign needs to be blacked out.
# Is obtained by multiplying image by binary mask.
img_pil = Image.open('/path/to/image.jpg')

# Instanciate:
textreader = TextReader(print_flag=True)

# Run:
scontent = textreader(img_pil)

# Display result:
print(scontent)