from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load an image from a URL or local path
#image_url = r"https://images.emedicinehealth.com/images/image_collection/skin/xerosis.jpg" # Replace with your image URL
image_url ="https://images.emedicinehealth.com/images/image_collection/skin/nummular-eczema.jpg"
image = Image.open(requests.get(image_url, stream=True).raw)

# Process the image and generate text
inputs = processor(images=image, return_tensors="pt")
outputs = model.generate(**inputs)
caption = processor.decode(outputs[0], skip_special_tokens=True)

print("Generated Caption:", caption)
