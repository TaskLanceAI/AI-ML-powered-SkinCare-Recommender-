import os
from PIL import Image, ImageDraw, ImageFont
from transformers import BlipProcessor, BlipForConditionalGeneration

# Define the directory containing the images
image_dir = r'C:\Users\meshram_a\source\repos\SkinDetection\Dataset\Eczema\Train\test'

# Load BLIP model and processor
model_name = "Salesforce/blip-image-captioning-base"
processor = BlipProcessor.from_pretrained(model_name)
model = BlipForConditionalGeneration.from_pretrained(model_name)

# Function to generate description using BLIP
def generate_description(image_path):
    with open(image_path, "rb") as image_file:
        image = Image.open(image_file).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    outputs = model.generate(**inputs)
    description = processor.decode(outputs[0], skip_special_tokens=True)
    return description

# Function to add description to an image
def add_description_to_image(image_path, description, output_path):
    # Open an image file
    with Image.open(image_path) as img:
        # Initialize ImageDraw
        draw = ImageDraw.Draw(img)
        # Use a truetype font
        font = ImageFont.load_default()
        # Position for the description
        text_position = (10, 10)
        # Add text to image
        draw.text(text_position, description, font=font, fill="white")
        # Save the edited image
        img.save(output_path)

# Iterate over all images in the directory
for filename in os.listdir(image_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(image_dir, filename)
        output_path = os.path.join(image_dir, "annotated_" + filename)
        description = generate_description(image_path)
        add_description_to_image(image_path, description, output_path)