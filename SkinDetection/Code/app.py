import streamlit as st
from tensorflow import keras # type: ignore
from PIL import Image
import numpy as np
    streamlit
    tensorflow
    Pillow
    numpy
import tensorflow as tf
import json

# Set page config
st.set_page_config(page_title="Skin Condition Classifier", layout="wide")

@st.cache_resource
def create_model():
    """Recreate the model architecture programmatically"""
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    
    # Compile the model
    model.compile(optimizer='adam',
                 loss='binary_crossentropy',
                 metrics=['accuracy'])
    return model

@st.cache_resource
def load_model():
    try:
        # Create model with same architecture
        model = create_model()
        
        # Load weights
        try:
            model.load_weights("model.weights.h5")
            return model
        except Exception as weight_error:
            st.error(f"Error loading weights: {str(weight_error)}")
            return None
            
    except Exception as e:
        st.error(f"Error setting up model: {str(e)}")
        return None

def preprocess_image(img):
    try:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Resize to match training dimensions
        img = img.resize((224, 224))
        
        # Convert to array and preprocess
        img_array = np.array(img)
        img_array = img_array / 255.0  # Same rescaling as in training
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        st.error(f"Error preprocessing image: {str(e)}")
        return None

def main():
    st.title("Skin Condition Classifier")
    st.write("Upload an image to classify between Eczema and Dry Skin")
    
    # Load model
    model = load_model()
    
    if model is None:
        st.error("""
        Failed to load model. Please ensure 'model_weights.h5' exists in the same directory.
        """)
        return
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            # Display the uploaded image
            col1, col2 = st.columns(2)
            
            with col1:
                img = Image.open(uploaded_file)
                st.image(img, caption='Uploaded Image', use_column_width=True)
            
            # Preprocess the image
            processed_img = preprocess_image(img)
            
            if processed_img is not None:
                # Make prediction
                with st.spinner('Analyzing image...'):
                    predictions = model.predict(processed_img)
                    predicted_class = 'Eczema' if predictions[0][0] > 0.5 else 'Dry Skin'
                    confidence = predictions[0][0] if predictions[0][0] > 0.5 else 1 - predictions[0][0]
                
                with col2:
                    st.subheader("Prediction Results")
                    st.write(f"Diagnosed Condition: **{predicted_class}**")
                    st.write(f"Confidence: **{confidence*100:.2f}%**")
                    
                    # Add disclaimer
                    st.warning("""
                    **Disclaimer**: This is an AI-assisted diagnosis tool and should not be used as a substitute 
                    for professional medical advice. Please consult a healthcare provider for proper diagnosis 
                    and treatment.
                    """)
        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            st.write("Please try uploading a different image.")

if __name__ == "__main__":
    main()