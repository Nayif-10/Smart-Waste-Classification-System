<<<<<<< HEAD
import cv2
import serial
import time
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the trained model (ensure this file exists)
model = tf.keras.models.load_model("final_model.h5")

# Setup serial communication with Arduino (adjust COM port if needed)
arduino = serial.Serial('COM3', 9600)  # Use correct port like COM4 or /dev/ttyUSB0
time.sleep(2)  # Allow time for Arduino to reset

# Setup camera (0 or 1 depending on webcam index)
cap = cv2.VideoCapture(1)

def classify(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Resize to model input
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    prediction = model.predict(img_array)
    return "metal" if prediction[0][0] < 0.5 else "plastic"

while True:
    if arduino.in_waiting > 0:
        message = arduino.readline().decode().strip()
        print(f"Received from Arduino: {message}")

        if message == "Object detected":
            print("Capturing image...")

            # Wait a bit before capturing
            time.sleep(2)

            ret, frame = cap.read()
            if ret:
                img_path = "captured.jpg"
                cv2.imwrite(img_path, frame)
                print("Image captured.")

                result = classify(img_path)
                print(f"Classified as: {result}")

                # Send result to Arduino
                arduino.write((result + "\n").encode())
                time.sleep(1)
            else:
                print("Failed to capture image.")

# Release camera on exit
cap.release()
cv2.destroyAllWindows()
=======
import cv2
import serial
import time
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the trained model (ensure this file exists)
model = tf.keras.models.load_model("final_model.h5")

# Setup serial communication with Arduino (adjust COM port if needed)
arduino = serial.Serial('COM3', 9600)  # Use correct port like COM4 or /dev/ttyUSB0
time.sleep(2)  # Allow time for Arduino to reset

# Setup camera (0 or 1 depending on webcam index)
cap = cv2.VideoCapture(1)

def classify(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Resize to model input
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    prediction = model.predict(img_array)
    return "metal" if prediction[0][0] < 0.5 else "plastic"

while True:
    if arduino.in_waiting > 0:
        message = arduino.readline().decode().strip()
        print(f"Received from Arduino: {message}")

        if message == "Object detected":
            print("Capturing image...")

            # Wait a bit before capturing
            time.sleep(2)

            ret, frame = cap.read()
            if ret:
                img_path = "captured.jpg"
                cv2.imwrite(img_path, frame)
                print("Image captured.")

                result = classify(img_path)
                print(f"Classified as: {result}")

                # Send result to Arduino
                arduino.write((result + "\n").encode())
                time.sleep(1)
            else:
                print("Failed to capture image.")

# Release camera on exit
cap.release()
cv2.destroyAllWindows()
>>>>>>> 0c6dfef (Initial project upload)
