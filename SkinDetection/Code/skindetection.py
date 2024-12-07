# Install necessary packages if not already installed
# %pip install transformers torch PIL cassandra-driver

import os
import torch
from PIL import Image
from io import BytesIO
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from transformers import CLIPProcessor, CLIPModel

# Initialize CLIP model and processor from Hugging Face
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# AstraDB details from environment variables
astra_db_token = os.getenv('ASTRA_DB_TOKEN_practice')
astra_db_secure_connect_bundle = os.getenv('ASTRA_DB_SECURE_CONNECT_practice')

# Function to get image embeddings using CLIP
def get_clip_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)
    return embedding[0].tolist()  # Convert tensor to list for storage

# Connect to AstraDB using the secure connect bundle
cloud_config = {
    'secure_connect_bundle': astra_db_secure_connect_bundle
}
auth_provider = PlainTextAuthProvider('token', astra_db_token)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# Define keyspace and table
keyspace = 'dbtraining'
table = 'skinembeddings'


session.execute(f"""
    CREATE TABLE IF NOT EXISTS {keyspace}.{table} (
        image_id UUID PRIMARY KEY,
        image_name TEXT,
        embedding VECTOR<float, 512>,  -- adjust dimensions if necessary
        metadata TEXT
    )
""")

# Function to store image embedding and metadata in AstraDB
def store_embedding_in_astra(image_name, embedding, metadata="{}"):
    query = f"""
    INSERT INTO {keyspace}.{table} (image_id, image_name, embedding, metadata)
    VALUES (uuid(), %s, %s, %s)
    """
    session.execute(query, (image_name, embedding, metadata))

# Example usage
image_paths = [
    r"C:\Users\meshram_a\source\repos\SkinDetection\Dataset\Eczema\Train\test\eczema.jpg",
    r"C:\Users\meshram_a\source\repos\SkinDetection\Dataset\Eczema\Train\test\atopic.jpg"
]

for image_path in image_paths:
    image_name = os.path.basename(image_path)
    embeddings = get_clip_image_embedding(image_path)  # Get the image embedding using CLIP
    
    # Format metadata if any additional details are needed
    metadata = '{"description": "Sample image metadata"}'
    
    # Store embedding and metadata in AstraDB
    store_embedding_in_astra(image_name, embeddings, metadata)
    print(f"Stored embedding for {image_name} in AstraDB.")
