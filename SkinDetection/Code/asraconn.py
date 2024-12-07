import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

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

# Initialize AstraDB session and get database details
session, database, keyspace = connect_astra()
print(f"Using database: {database}, Keyspace: {keyspace}")
