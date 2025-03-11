import cv2
import numpy as np
import imutils
import requests  # Import requests to send data to ESP32

# ESP32 IP Address (Change this based on your ESP32 Serial Monitor output)
ESP_IP = "http://192.168.131.254"  # Replace with your ESP32’s actual IP

# Load the MobileNet SSD model
prototxt = r"C:\Users\amzad\OneDrive\Desktop\Home Automation\deploy.prototxt"
model = r"C:\Users\amzad\OneDrive\Desktop\Home Automation\mobilenet_iter_73000.caffemodel"

net = cv2.dnn.readNetFromCaffe(prototxt, model)

# Define the class labels MobileNet SSD was trained on
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant",
           "sheep", "sofa", "train", "tvmonitor"]

# Initialize Video Capture
cap = cv2.VideoCapture(0)  # 0 for webcam

device_on = False  # Track ESP32 device state

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=600)
    h, w = frame.shape[:2]

    # Convert frame to blob format
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    person_count = 0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Consider only high-confidence detections
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])

            if CLASSES[idx] == "person":
                person_count += 1
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Draw bounding box around person
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                text = f"Person: {confidence * 100:.2f}%"
                cv2.putText(frame, text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Send ON/OFF signals to ESP32 based on person detection
    if person_count > 0 and not device_on:
        requests.get(f"{ESP_IP}/control?state=1")  # Send ON command
        device_on = True
        print("Sent ON signal to ESP32")
    elif person_count == 0 and device_on:
        requests.get(f"{ESP_IP}/control?state=0")  # Send OFF command
        device_on = False
        print("Sent OFF signal to ESP32")

    # Display count on the frame
    cv2.putText(frame, f"People Count: {person_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Person Detection", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
