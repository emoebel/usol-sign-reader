import moondream as md
from PIL import Image

# This will run the model locally
#model = md.vl(endpoint="http://localhost:2020/v1")
model = md.vl(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI0MDQ2ZDljNi1iNjA4LTQ2NmItODFiNS03NTc5YTJjOTUxMTQiLCJvcmdfaWQiOiJaQkZoUHNyNjJtQVRvSnpKa3c3TktCZGhieGNvelg1cyIsImlhdCI6MTc1MDE2OTIyMSwidmVyIjoxfQ.-WxqicYJ2XEvAKyhiEjxkgwdW1wRR64FFX4x_AmZvD0")

# Load your image
#image = Image.open("/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_3.png")
image = Image.open("/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_2.png")

# 2. Visual Question Answering
answer = model.query(image, "Give me the name of the destinations and their durations")['answer']
print(answer)