import cv2
import os

# Paths
SAMPLES_DIR = "engine/auth/samples"
USERS_FILE = "engine/auth/users.txt"

# Ensure folders exist
os.makedirs(SAMPLES_DIR, exist_ok=True)
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

# --- Step 1: Get user info
face_id = input("Enter a numeric user ID: ").strip()
user_name = input("Enter your name: ").strip()

# --- Step 2: Save to users.txt (avoid duplicates)
def update_user_list(face_id, user_name):
    updated = False
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith(f"{face_id}="):
                lines[i] = f"{face_id}={user_name}\n"
                updated = True
                break
        if not updated:
            lines.append(f"{face_id}={user_name}\n")
        with open(USERS_FILE, "w") as f:
            f.writelines(lines)
    else:
        with open(USERS_FILE, "w") as f:
            f.write(f"{face_id}={user_name}\n")

update_user_list(face_id, user_name)

# --- Step 3: Start capturing images
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)  # Frame width
cam.set(4, 480)  # Frame height

detector = cv2.CascadeClassifier('engine/auth/haarcascade_frontalface_default.xml')

print("Taking samples, look at the camera...")

count = 0
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face_img = gray[y:y + h, x:x + w]
        cv2.imwrite(f"{SAMPLES_DIR}/face.{face_id}.{count}.jpg", face_img)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:  # ESC
        break
    elif count >= 100:  # Stop after 100 samples
        break

print("✅ Samples captured successfully!")
cam.release()
cv2.destroyAllWindows()
