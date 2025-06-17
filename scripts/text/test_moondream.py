from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

# Load the model
model = AutoModelForCausalLM.from_pretrained(
    "vikhyatk/moondream2",
    revision="2025-01-09",
    trust_remote_code=True,  # Uncomment for GPU acceleration & pip install accelerate # device_map={"": "cuda"}
)

# Load your image
image = Image.open("/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_3.png")


# 2. Visual Question Answering
print("Asking questions about the image:")
print(model.query(image, "Give me the name of the destinations and their durations")["answer"])
