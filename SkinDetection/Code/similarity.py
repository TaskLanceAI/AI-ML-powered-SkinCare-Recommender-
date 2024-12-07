import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

os.system('cls' if os.name == 'nt' else 'clear')


# Path to your Secure Connect Bundle
secure_connect_bundle_path = 'C:/Users/meshram_a/source/repos/SkinDetection/Credentials/secure-connect-biomedical.zip'

# Your application token
application_token = 'AstraCS:EJUQQhtupeEoHRHPhLmiNmoD:12209d1c8c954dac6a0f68cca9e54e1520f3e4b10cf22eee3c74b425ec7b28fe'


# Debug prints to check environment variables
print(f"Secure Connect Bundle Path: {secure_connect_bundle_path}")
print(f"Application Token: {application_token}")

# Check if the environment variables are loaded correctly
if not secure_connect_bundle_path or not os.path.exists(secure_connect_bundle_path):
    raise FileNotFoundError(f"Secure connect bundle not found at path: {secure_connect_bundle_path}")

if not application_token:
    raise ValueError("Application token not found in environment variables")

# Connect to the Cassandra database using the secure connect bundle
session = Cluster(
    cloud={"secure_connect_bundle": secure_connect_bundle_path},
    auth_provider=PlainTextAuthProvider("token", application_token),
).connect()

# Define keyspace and vector dimension
keyspace = "skintech"


# Function to get productdescvector by productid
def get_productdescvector(image_id):
    query = f"SELECT embedding FROM {keyspace}.skinimageembeddings WHERE image_id = {image_id}"
    row = session.execute(query).one()
    if row:
        return row.embedding
    else:
        raise ValueError(f"Image with id {image_id} not found")

#  image_id to find similar matches
image_id = 'debec872-a382-404c-976b-451c2f9e9364'

# Fetch the productdescvector for the given productid
embedding = get_productdescvector(image_id)

# Query to find similar matches using the fetched productdescvector
ann_query = (
    f"SELECT image_id, similarity_cosine(embedding, {embedding}) as similarity FROM {keyspace}.skinimageembeddings "
    f"ORDER BY embedding ANN OF {embedding} LIMIT 2"
)
for row in session.execute(ann_query):
    print(f"[{row.image_id}\" (sim: {row.similarity:.4f})")

print("Data with similar match.")
