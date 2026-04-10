import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Lambda, Conv2D, Dropout, Flatten, Dense
import cv2
import numpy as np

def build_nvidia_model():
    """
    NVIDIA End-to-End Learning for Self-Driving Cars architecture.
    """
    model = Sequential()
    
    # Preprocessing: Normalize and Crop
    model.add(Lambda(lambda x: x/127.5 - 1.0, input_shape=(66, 200, 3)))
    
    # Convolutional Layers
    model.add(Conv2D(24, (5, 5), strides=(2, 2), activation='elu'))
    model.add(Conv2D(36, (5, 5), strides=(2, 2), activation='elu'))
    model.add(Conv2D(48, (5, 5), strides=(2, 2), activation='elu'))
    model.add(Conv2D(64, (3, 3), activation='elu'))
    model.add(Conv2D(64, (3, 3), activation='elu'))
    
    model.add(Dropout(0.5))
    model.add(Flatten())
    
    # Fully Connected Layers
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    model.add(Dense(1)) # Output: Steering Angle
    
    model.compile(optimizer='adam', loss='mse')
    return model

def preprocess_image(img):
    # Resizing to NVIDIA architecture expected input
    img = img[60:135, :, :] # Crop hood and sky
    img = cv2.resize(img, (200, 66))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) # Improved feature extraction
    return img

if __name__ == "__main__":
    model = build_nvidia_model()
    model.summary()
    # model.save('models/steering_model.h5')
    print("Model Architecture Built Successfully!")
