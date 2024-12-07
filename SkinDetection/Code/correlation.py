from tensorflow.keras.layers import Input, Dense, Flatten, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.applications import VGG16

# Image model
image_input = Input(shape=(150, 150, 3))
base_model = VGG16(weights='imagenet', include_top=False)(image_input)
flat_image = Flatten()(base_model)

# Blood marker model
blood_marker_input = Input(shape=(5,))  # assuming 5 blood markers as input features
blood_dense = Dense(64, activation='relu')(blood_marker_input)

# Combine image and blood marker features
combined = Concatenate()([flat_image, blood_dense])
final_dense = Dense(64, activation='relu')(combined)
output = Dense(1, activation='sigmoid')(final_dense)

# Create model
model = Model(inputs=[image_input, blood_marker_input], outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(
    [image_data, blood_marker_data],  # image and blood marker arrays
    labels,  # target labels
    validation_data=([val_image_data, val_blood_marker_data], val_labels),
    epochs=10,
    batch_size=32
)
