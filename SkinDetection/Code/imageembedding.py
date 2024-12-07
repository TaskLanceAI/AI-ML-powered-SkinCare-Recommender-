# Install necessary packages
# %pip install openai

import openai

# Set up your OpenAI API key
openai.api_key = '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'

# Function to get embeddings using OpenAI's model
def get_openai_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(input=[text], model=model)
    return response['data'][0]['embedding']

# List of product descriptions
product_descriptions = [
    "Under colors of Benetton Men White Boxer Trunks",
    "Turtle Men Check Red Shirt"
]

# Iterate over each product description
for i, product_desc in enumerate(product_descriptions, start=1):
    # Get embeddings for the current product description using OpenAI
    embeddings = get_openai_embedding(product_desc)
    
    # Format the embeddings to a specific format, e.g., printing the first 5 elements
    formatted_embeddings = '[' + ', '.join(f"{emb:.16f}" for emb in embeddings[:5]) + ']'
    
    # Prepare and print the output in the specified format
    output = f"{i},{product_desc},{formatted_embeddings}"
    print(output)
