import cv2
import os
import time


# Load user ID → name mapping from users.txt
def load_names(file_path='engine/auth/users.txt'):
    names = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    id_str, name = line.strip().split('=')
                    names[int(id_str)] = name
    return names


def AuthenticateFace():
    flag = 0  # Default to failure

    model_path = 'engine/auth/trainer/trainer.yml'
    samples_path = 'engine/auth/samples'

    # Check if model and samples exist
    if not os.path.exists(model_path):
        print("[ERROR] Trainer model not found.")
        return 0
    if not os.listdir(samples_path):
        print("[ERROR] No sample data found.")
        return 0

    # Load trained model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)

    # Load Haar Cascade for face detection
    cascadePath = "engine/auth/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    # Load ID-to-name mapping
    names = load_names()

    # Start camera
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  # Frame width
    cam.set(4, 480)  # Frame height

    # Define min face size for detection
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    font = cv2.FONT_HERSHEY_SIMPLEX

    print("[INFO] Starting face recognition. Look at the camera...")

    start_time = time.time()
    while True:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:
            roi = gray[y:y + h, x:x + w]
            id, confidence = recognizer.predict(roi)

            # Default to unknown
            name = "Unknown"
            confidence_text = f"{round(100 - confidence)}%"

            # Only succeed if confidence is good AND name exists
            if confidence < 60 and id in names:
                name = names[id]
                flag = 1  # ✅ Authentication success

            # Draw rectangle and text
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence_text), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('Face Authentication', img)

        k = cv2.waitKey(10) & 0xff
        if k == 27 or flag == 1:
            break

        # Optional timeout
        if time.time() - start_time > 15:
            print("[INFO] Authentication timeout.")
            break

    cam.release()
    cv2.destroyAllWindows()

    return flag
