import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.models import Model

# Define the directory containing the images
image_dir = r'C:\Users\meshram_a\source\repos\SkinDetection\Dataset\Eczema\Train\test'

# Load the pre-trained model and extract features from a layer close to the output layer
base_model = InceptionV3(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)

def get_image_embedding(img_path):
    """Function to get the embedding for a single image."""
    img = image.load_img(img_path, target_size=(299, 299))  # Resizing image to fit InceptionV3 input size
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    
    # Generate embeddings using the model
    embedding = model.predict(img_data)
    return embedding.flatten()

def get_embeddings_for_folder(folder_path):
    """Function to get embeddings for all images in a specified folder."""
    embeddings = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            embeddings[filename] = get_image_embedding(img_path)
            print(f"Processed {filename}")
    return embeddings

# Generate embeddings for images in the specified directory
embeddings = get_embeddings_for_folder(image_dir)

# Optional: Save embeddings to a file for future use
np.save('image_embeddings.npy', embeddings)  # Saves as a NumPy .npy file
print("Embeddings generated and saved to 'image_embeddings.npy'")
