from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load an image from a local path
image_path = r"C:\Users\meshram_a\source\repos\SkinDetection\Dataset\Eczema\Train\bcef.jpg"  # Replace with your image file name
image = Image.open(image_path)

# Process the image and generate text
inputs = processor(images=image, return_tensors="pt")
outputs = model.generate(**inputs)
caption = processor.decode(outputs[0], skip_special_tokens=True)

print("Generated Caption:", caption)


