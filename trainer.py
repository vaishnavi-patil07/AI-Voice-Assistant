import cv2
import numpy as np
from PIL import Image #pillow package
import os

path = 'engine\\auth\\samples' # Path for samples already taken

recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
detector = cv2.CascadeClassifier("engine\\auth\\haarcascade_frontalface_default.xml")
#Haar Cascade classifier is an effective object detection approach


def Images_And_Labels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)
                  if f.endswith(('.jpg', '.jpeg', '.png'))]  # Only load images

    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        try:
            gray_img = Image.open(imagePath).convert('L')  # Convert to grayscale
            img_arr = np.array(gray_img, 'uint8')

            # Expect filename format: face.<id>.<count>.jpg
            id = int(os.path.split(imagePath)[-1].split(".")[1])

            faces = detector.detectMultiScale(img_arr)

            for (x, y, w, h) in faces:
                faceSamples.append(img_arr[y:y + h, x:x + w])
                ids.append(id)
        except Exception as e:
            print(f"[WARNING] Skipped {imagePath} — {e}")

    return faceSamples, ids

print ("Training faces. It will take a few seconds. Wait ...")

faces,ids = Images_And_Labels(path)
if not faces or not ids:
    print("[ERROR] No valid data to train. Make sure sample images exist and are valid.")
    exit()
recognizer.train(faces, np.array(ids))

recognizer.write('engine\\auth\\trainer\\trainer.yml')  # Save the trained model as trainer.yml

print("Model trained, Now we can recognize your face.")