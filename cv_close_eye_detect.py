import cv2
import time
import serial

# Load Haar cascades for face and eye detection
eye_cascPath = '/home/zxcv/anti_sleep_glasses/Closed-Eye-Detection-with-opencv/haarcascade_eye_tree_eyeglasses.xml'
face_cascPath = '/home/zxcv/anti_sleep_glasses/Closed-Eye-Detection-with-opencv/haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(face_cascPath)
eyeCascade = cv2.CascadeClassifier(eye_cascPath)

# Connect to ESP32 (adjust your serial port if needed)
esp = serial.Serial('/dev/ttyUSB0', 115200)  # e.g., COM3 on Windows or /dev/ttyUSB0 on Linux

# Open webcam
cap = cv2.VideoCapture(0)

# Eye closed timing
eye_closed_start_time = None
eye_closed_duration = 1  # seconds

while True:
    ret, img = cap.read()
    if ret:
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            roi_gray = frame[y:y + h, x:x + w]
            eyes = eyeCascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
            )

            if len(eyes) == 0:
                print("No eyes detected")
                if eye_closed_start_time is None:
                    eye_closed_start_time = time.time()
                elif time.time() - eye_closed_start_time >= eye_closed_duration:
                    print("⚠️ Eyes closed for more than 10 seconds!")
                    esp.write(b'1')  # Turn GND ON → device ON
            else:
                print("Eyes detected")
                eye_closed_start_time = None
                esp.write(b'0')  # Turn GND OFF → device OFF

            resized = cv2.resize(img[y:y + h, x:x + w], (500, 500))
            cv2.imshow('Face & Eye Detection', resized)

        if cv2.waitKey(1) in [ord('q'), ord('Q')]:
            break

# Cleanup
cap.release()
cv2.destroyAllWindows()
esp.close()
