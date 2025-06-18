import moondream as md
from PIL import Image

# This will run the model locally
#model = md.vl(endpoint="http://localhost:2020/v1")
model = md.vl(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI0MDQ2ZDljNi1iNjA4LTQ2NmItODFiNS03NTc5YTJjOTUxMTQiLCJvcmdfaWQiOiJaQkZoUHNyNjJtQVRvSnpKa3c3TktCZGhieGNvelg1cyIsImlhdCI6MTc1MDE2OTIyMSwidmVyIjoxfQ.-WxqicYJ2XEvAKyhiEjxkgwdW1wRR64FFX4x_AmZvD0")

# Load your image
#image = Image.open("/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_3.png")
#image = Image.open("/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_2.png")
#image = Image.open("/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_1.png")
image = Image.open("/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_4.png")

# 2. Visual Question Answering
answer = model.query(image, "Give me the name of the destinations and their durations")['answer']
#answer = model.query(image, "For each text line, give me the name of the destination and the corresponding duration")['answer']
#answer = model.query(image, "This image contains text lines, where each line corresponds to a destination and a duration. Give me the destination and duration pairs")['answer']
#answer = model.query(image, "In this image each text line corresponds to a destination and a duration pair. Give me the content of each line")['answer']
#answer = model.query(image, "This image contains a table where the first column is a destination, and the second column a duration. Give me the content of each row")['answer']
print(answer)