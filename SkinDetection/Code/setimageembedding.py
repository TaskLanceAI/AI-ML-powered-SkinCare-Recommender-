import os
import requests
import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Get environment variables
astra_db_token = os.getenv('ASTRA_DB_TOKEN_practice')
astra_db_secure_connect_bundle = os.getenv('ASTRA_DB_SECURE_CONNECT_practice')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Connect to the Cassandra database using the secure connect bundle
cloud_config = {
    'secure_connect_bundle': astra_db_secure_connect_bundle
}
auth_provider = PlainTextAuthProvider('token', astra_db_token)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# Define keyspace and table
keyspace = 'dbtraining'
table = 'skin'

# Description for the movie
description = (
    "Marty McFly, a 17-year-old high school student, is accidentally sent 30 years into the past "
    "in a time-traveling DeLorean invented by his close friend, the maverick scientist Doc Brown."
)

# Function that generates embeddings
def embedding(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    response = requests.post("https://api.openai.com/v1/embeddings", headers=headers, data=json.dumps(data))
    response_data = response.json()
    return response_data['data'][0]['embedding']

# Get the embedding for the description
skinvector = embedding(description)

# Insert the movie document into Cassandra
insert_query = f"""
INSERT INTO {keyspace}.{table} (id,title, year, genre, description, skinvector)
VALUES (%s,%s, %s, %s, %s, %s)
"""

# Execute the query
print (insert_query)
session.execute(insert_query, (1,"Back to the Future", "1985", "Comedy", description, skinvector))
