# Install necessary packages (run this if not installed)
# %pip install cassandra-driver
# %pip install openai
# %pip install PIL

import os
import openai
import base64
from PIL import Image
from io import BytesIO
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Replace with your actual OpenAI API key if not using environment variables

# AstraDB details from environment variables
secure_connect_bundle_path = os.getenv('ASTRA_DB_SECURE_CONNECT_practice')
application_token = os.getenv('ASTRA_DB_TOKEN_practice')
KEYSPACE = "dbtraining"  # Replace with your actual keyspace name

def connect_astra():
    cloud_config = {
        'secure_connect_bundle': secure_connect_bundle_path
    }
    auth_provider = PlainTextAuthProvider('token', application_token)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect(KEYSPACE)
    
    database_name = "practice"
    print(f"Connected to database: {database_name}, Keyspace: {KEYSPACE}")
    return session, database_name, KEYSPACE

# Function to get embeddings using OpenAI's CLIP model for images
def get_openai_image_embedding(image_path):
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    
    response = openai.Image.create(image=image_b64, model="clip-vision-base-patch32")
    return response['data'][0]['embedding']

# Set up AstraDB connection
def connect_astra():
    cloud_config = {
        'secure_connect_bundle': secure_connect_bundle_path
    }
    auth_provider = PlainTextAuthProvider('token', application_token)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    return session

# Initialize AstraDB session
session = connect_astra()

# Ensure the keyspace and table are available
KEYSPACE = "dbtraining"
TABLE = "embeddings"
session.execute(f"""
    CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
    WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
""")
session.execute(f"""
    CREATE TABLE IF NOT EXISTS {KEYSPACE}.{TABLE} (
        image_id UUID PRIMARY KEY,
        image_name TEXT,
        embedding VECTOR<float, 512>,  -- adjust dimensions if necessary
        metadata TEXT
    )
""")

# Function to store image embedding and metadata in AstraDB
def store_embedding_in_astra(image_name, embedding, metadata="{}"):
    query = f"""
    INSERT INTO {KEYSPACE}.{TABLE} (image_id, image_name, embedding, metadata)
    VALUES (uuid(), %s, %s, %s)
    """
    session.execute(query, (image_name, embedding, metadata))

# Example usage
image_paths = [r"C:\Users\meshram_a\source\repos\SkinDetection\Dataset\Eczema\Train\test\eczema_in_babies_and_children.jpg"]

#image_paths = ["C:\Users\meshram_a\source\repos\SkinDetection\Dataset\Eczema\Train\test\eczema_in_babies_and_children.jpg"]  # Replace with actual image paths

for image_path in image_paths:
    image_name = os.path.basename(image_path)
    embeddings = get_openai_image_embedding(image_path)  # Get the image embedding
    
    # Format metadata if any additional details are needed
    metadata = '{"description": "Sample image metadata"}'
    
    # Store embedding and metadata in AstraDB
    store_embedding_in_astra(image_name, embeddings, metadata)
    print(f"Stored embedding for {image_name} in AstraDB.")
