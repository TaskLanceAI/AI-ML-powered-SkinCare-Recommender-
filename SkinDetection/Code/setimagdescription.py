# Install necessary packages if not already installed
# %pip install transformers torch PIL cassandra-driver

import os
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Initialize CLIP model and processor from Hugging Face
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# AstraDB details from environment variables
# astra_db_token = os.getenv('ASTRA_DB_TOKEN_practice')
#astra_db_secure_connect_bundle = os.getenv('ASTRA_DB_SECURE_CONNECT_practice')

# Path to your Secure Connect Bundle
astra_db_secure_connect_bundle = 'C:/Users/meshram_a/source/repos/SkinDetection/Credentials/secure-connect-biomedical.zip'

# Your application token
astra_db_token = 'AstraCS:EJUQQhtupeEoHRHPhLmiNmoD:12209d1c8c954dac6a0f68cca9e54e1520f3e4b10cf22eee3c74b425ec7b28fe'


# Folder containing images
#image_folder = r"C:\Users\meshram_a\source\repos\SkinDetection\Dataset\Eczema\Train"
image_folder = r"C:\Users\meshram_a\source\repos\SkinDetection\Dataset\Not eczema\Train"

# Function to get image embeddings using CLIP
def get_clip_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)
    return embedding[0].tolist()  # Convert tensor to list for storage

# Placeholder function to generate descriptions for images (implement with a model if desired)
def generate_image_description(image_name):
    # Replace this with actual description generation logic if available
    return f"Description for image {image_name}"

# Connect to AstraDB using the secure connect bundle
cloud_config = {
    'secure_connect_bundle': astra_db_secure_connect_bundle
}
auth_provider = PlainTextAuthProvider('token', astra_db_token)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# Define keyspace and table
keyspace = 'skintech'
table = 'skinimageembeddings'


session.execute(f"""
    CREATE TABLE IF NOT EXISTS {keyspace}.{table} (
        image_id UUID PRIMARY KEY,
        image_name TEXT,
        embedding VECTOR<float, 512>,  -- adjust dimensions if necessary
        label TEXT,
        metadata TEXT
    )
""")

# Function to store image embedding, description, and metadata in AstraDB
def store_embedding_in_astra(image_name, embedding, label, metadata="{}"):
    query = f"""
    INSERT INTO {keyspace}.{table} (image_id, image_name, embedding, label, metadata)
    VALUES (uuid(), %s, %s, %s, %s)
    """
    session.execute(query, (image_name, embedding, label, metadata))

# Load all images from the specified folder
for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        image_path = os.path.join(image_folder, filename)
        
        # Generate image embedding
        embedding = get_clip_image_embedding(image_path)
        
        # Generate description for the image
        description = generate_image_description(filename)
        
        # Store embedding, description, and metadata in AstraDB
        metadata = '{"label": "Not Eczema"}'  # You can modify metadata as needed
        store_embedding_in_astra(filename, embedding, description, metadata)
        print(f"Stored embedding for {filename} in AstraDB with description: {description}")
