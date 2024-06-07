import os
import tensorflow as tf
import numpy as np
from keras.preprocessing import image

def predict(img_path):
    labels = {0: 'Cardboard', 1: 'Glass', 2: 'Metal', 3: 'Paper', 4: 'Plastic', 5: 'Trash'}
    img = image.load_img(img_path, target_size=(300, 300))  # Change to 300, 300
    img = image.img_to_array(img, dtype=np.uint8)
    img = np.array(img) / 255.0
    model = tf.keras.models.load_model("trained_model.h5")
    predicted = model.predict(img[np.newaxis, ...])
    prob = np.max(predicted[0], axis=-1) * 100
    prob = round(prob, 2)
    predicted_class = labels[np.argmax(predicted[0], axis=-1)]

    if predicted_class in ['Cardboard', 'Paper']:
        category = "Biodegradable"
    elif predicted_class in ['Metal', 'Glass', 'Plastic']:
        category = "Non-Biodegradable"
    else:
        category = "Categorizing Difficult"

    return category, predicted_class, f"{prob}%"
