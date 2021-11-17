import cv2
import mediapipe as mp
import numpy as np
import dlib
import sys

# haarcascade
cascPath = "/home/alyr/PycharmProjects/Subcognition/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

# OpenCV DNN

DNN = "TF" # Or CAFFE, or any other suported framework
min_confidence = 0.5 # minimum probability to filter weak detections
modelFile = "opencv_face_detector_uint8.pb"
configFile = "opencv_face_detector.pbtxt"
# Here we need to read our pre-trained neural net created using Tensorflow
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

# dlib

face_detect = dlib.cnn_face_detection_model_v1("/home/alyr/PycharmProjects/Subcognition/models/content/mmod_human_face_detector.dat")

# Mediapipe

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def face_detection_haarcascade(frame):
    global faceCascade
    faces = faceCascade.detectMultiScale2(frame, scaleFactor=1.1, minNeighbors=5, flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, w, h) in faces[0]:
        conf = faces[1][0][0]
        if conf > 5:
            text = f"{conf * 10:.2f}%"
            cv2.putText(frame, text, (x, y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (170, 170, 170), 1)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)
    return frame, faces


def face_detection_DNN(frame):
    # Our operations on the frame come here
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame1 = cv2.resize(frame, (int(600), int(400)))

    blob = cv2.dnn.blobFromImage(cv2.resize(frame1, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    (h, w) = frame1.shape[:2]
    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > min_confidence:
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the bounding box of the face along with the associated
            # probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame1, (startX, startY), (endX, endY),
                          (0, 0, 255), 2)
            # (0,0,255) - red color
            cv2.putText(frame1, text, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    return frame1, detections


def face_detection_dlib(frame):
    faces = face_detect(frame, 1)
    for face in faces:
        # In dlib in order to extract points we need to do this
        x1 = face.rect.left()
        y1 = face.rect.bottom()
        x2 = face.rect.right()
        y2 = face.rect.top()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
    # show the output frame
    return frame, faces

def face_detection_mediapipe(frame):
    with mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5) as face_detection:
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame)
        # return results
        # Draw the face detection annotations on the image.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(frame, detection)
        # Flip the image horizontally for a selfie-view display.
        return frame, results.detections