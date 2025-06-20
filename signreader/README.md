# ImageReader
This class contains the whole image processing pipeline. 
It calls 3 different AI models that can be found in 
`engine.segmentation.sign.SignDetector`, 
`engine.segmentation.symbol.SymbolDetector`, 
and `engine.segmentation.text.TextReader`.

Below how to instanciate `ImageReader` and use it to process an image:
```
from signreader.detector import ImageReader
from PIL import Image

img_pil = Image.open('/path/to/image.jpg') # open image
ireader = ImageReader() # instanciate
icontent = ireader(img_pil) # run pipeline
```

# SignDetector
This model achieves instance segmentation using [Cellpose](https://github.com/MouseLand/cellpose).
```
from signreader.engine.sign import SignDetector
from PIL import Image
import numpy as np

img_np = np.asarray(Image.open('/path/to/image.jpg')) # open image
signdetector = SignDetector() # instanciate
masks = signdetector(img_np) # run model
```

# SymbolDetector
This model achieves bounding box object detection, using [Ultralytics](https://github.com/ultralytics/ultralytics).
```
from signreader.engine.symbol import SymbolDetector
from PIL import Image
import numpy as np

img_np = np.asarray(Image.open('/path/to/image.jpg')) # open image
symbdetector = SymbolDetector() # instanciate
boxes, class_names = symbdetector(img_np) # run model
```

# TextReader
This model achieves optical character recognition (OCR), using [Moondream](https://github.com/vikhyat/moondream).
In other words, it allows to transcribe the text in images.
Moondream is a general visual language model that understands images using text prompts.
It can achieve multiple tasks, such as:
- Image captioning (input: image, output: text)
- Visual question answering (inputs: image and text, output: text)
- Object detection (inputs: image and text, output: box coordinates)
- Pointing (inputs: image and text, output: point coordinates)

I'm using Moondream to detect and localize text in signs. 
For the current prototype, this allowed me to quickly access to a free OCR tool with acceptable performance.
However, in the future, Moondream should be replaced by a more specialised AI model.
While it has good performance for detecting text, it has troubles formating the output string correctly, 
and to understand which word is part of which text line. This causes all kind of errors when outputing the result in json.

While these kind of generalistic models produce impressive results on a variety of tasks, 
they fail at delivering high performance for a specific task. This is why I did not use
Moondream for detecting symbols and signs. However, in the frame of this prototype, 
it illustrates well the possibilities of using AI for analysing photos of hiking signs.

Moreover, Moondream needs a server to run. Currently I am using their cloud server with an
API key. But it can also run on a local server. More information [here](https://moondream.ai/c/docs/quickstart).