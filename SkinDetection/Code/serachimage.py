from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd

# Path to your Secure Connect Bundle
astra_db_secure_connect_bundle = 'C:/Users/meshram_a/source/repos/SkinDetection/Credentials/secure-connect-biomedical.zip'

# Your application token
astra_db_token = 'AstraCS:EJUQQhtupeEoHRHPhLmiNmoD:12209d1c8c954dac6a0f68cca9e54e1520f3e4b10cf22eee3c74b425ec7b28fe'

cloud_config = {
    'secure_connect_bundle': astra_db_secure_connect_bundle
}
auth_provider = PlainTextAuthProvider('token', astra_db_token)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
#session = cluster.connect()

# Define keyspace and table
keyspace = 'skintech'
session = cluster.connect(keyspace)



# Convert product_id to UUID
image_id = 'debec872-a382-404c-976b-451c2f9e9364'


query_fetch_vector = """
SELECT embedding
FROM skintech.skinimageembeddings
WHERE image_id = debec872-a382-404c-976b-451c2f9e9364
"""
result = session.execute(query_fetch_vector, (image_id,))
vector_row = result.one()

# Check if the vector was found, and store it in varvector
if vector_row:
    varvector = vector_row.embedding
else:
    print("No vector found for the specified product_id.")
    varvector = None

# Proceed only if varvector is populated
if varvector:
    # Second query using the fetched vector
    query_similarity = """
    SELECT
      image_id, image_name, label,
      similarity_cosine(%s, embedding) * 100 AS similarity
    FROM skintech.
    skinimageembeddings
    ORDER BY embedding ANN OF %s
    LIMIT 3
    """
    
    # Execute query and fetch results
    results = session.execute(query_similarity, (varvector, varvector))
    rows = [row for row in results]
    
    # Load results into DataFrame
    df = pd.DataFrame(rows)
    print(df)
else:
    print("Unable to retrieve vector for similarity comparison.")
