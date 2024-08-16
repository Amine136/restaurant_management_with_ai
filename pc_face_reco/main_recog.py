# Load Cameraimport cv2
from simple_facerec import SimpleFacerec
import cv2
import sys
import random
from db_operations import create_connection, save_face_event

#sys.path.append("C:\\Users\\HP\\Desktop\\flash\\stage\\pc_face_reco\\venv\\Lib\\site-packages\\face_recognition_models")

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Load Camera
cap = cv2.VideoCapture(0)  # Start with 0, change to 1 if it doesn't work

# Function to get a random event type
def get_random_event_type():
    return random.choice(['enters', 'exit'])

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        continue

    print(f"Frame shape: {frame.shape}")

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        # Save the face event to the database
        conn = create_connection()
        if conn:
            event_type = get_random_event_type()
            save_face_event(conn, name, event_type)
            conn.close()

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)  # Start with 0, change to 1 if it doesn't work

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        continue

    print(f"Frame shape: {frame.shape}")

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
