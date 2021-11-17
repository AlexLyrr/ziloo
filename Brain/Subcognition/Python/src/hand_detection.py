import cv2
import mediapipe as mp
import sys
import numpy as np
from src.yolo import YOLO
import math
# import pybgs as bgs  # This package is manually added
import pywt
import random as rng

# mediapipe variables
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

# rectangle variables
rectangle_top_left = [sys.maxsize, sys.maxsize]
rectangle_bottom_right = [0, 0]

# yolo variables
yolo = YOLO("models/cross-hands-yolov4-tiny.cfg",
            "models/cross-hands-yolov4-tiny.weights", ["hand"])
yolo.size = 150
yolo.confidence = 0.5

# fast variables
# there are many bgs algorithms for background subtraction,
# see https://github.com/andrewssobral/bgslibrary/blob/master/demo2.py
# algorithm = bgs.StaticFrameDifference()


class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])


class MediapipeHandItem:
    def __init__(self):
        self._top_left = [sys.maxsize, sys.maxsize]
        self._bottom_right = [0, 0]

    @property
    def top_left(self):
        return self._top_left

    @top_left.setter
    def top_left(self, value):
        self._top_left = value

    @property
    def bottom_right(self):
        return self._bottom_right

    @bottom_right.setter
    def bottom_right(self, value):
        self._bottom_right = value

    def calculate_box(self, landmark, image_width, image_height):
        # 1st approach
        # if you use this method, activate the rectangle extension!
        # for id, lm in enumerate(landmark):
        #     if id not in [0, 1, 5, 6, 9, 10, 13, 14, 17, 18]:
        #         self.top_left = np.minimum(self.top_left, [int(lm.x * image_width), int(lm.y * image_height)])
        #         self.bottom_right = np.maximum(self.bottom_right, [int(lm.x * image_width), int(lm.y * image_height)])
        # 2nd approach
        # If you use this method, deactivate the rectangle extension!!
        RECTANGLE_EXTENSION = Point(240, 224)
        thumb_p = (int(landmark[mpHands.HandLandmark.THUMB_IP].x * image_width), int(landmark[mpHands.HandLandmark.THUMB_IP].y * image_height))
        self.top_left = (thumb_p[0] - RECTANGLE_EXTENSION.x, thumb_p[1] - RECTANGLE_EXTENSION.y)
        self.bottom_right = (thumb_p[0] + RECTANGLE_EXTENSION.x, thumb_p[1])
        self.top_left = (
        np.clip(self.top_left[0], 0, image_width),
        np.clip(self.top_left[1], 0, image_height))
        self.bottom_right = (
            np.clip(self.bottom_right[0], 0, image_width),
            np.clip(self.bottom_right[1], 0, image_height))


def mediapipe_hand_detection(frame):
    global rectangle_top_left, rectangle_bottom_right
    frame_mediapipe = frame.copy()
    img_rgb = cv2.cvtColor(frame_mediapipe, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    image_height, image_width, _ = frame_mediapipe.shape
    no_hands = 0
    hand_center = []
    hand_label = []
    mediapipeHandItem = MediapipeHandItem()
    if results.multi_hand_landmarks:
        no_hands = len(results.multi_hand_landmarks)
        # Iterate for all hands found
        for handLm in results.multi_hand_landmarks:
            # Draw landmarks
            mpDraw.draw_landmarks(frame_mediapipe, handLm, mpHands.HAND_CONNECTIONS)
            # print('hand_landmarks:', handLm)
            rectangle_top_left = [sys.maxsize, sys.maxsize]
            rectangle_bottom_right = [0, 0]
            # print(
            #     f'Index finger tip coordinates: (',
            #     f'{handLm.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
            #     f'{handLm.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
            # )
            mediapipeHandItem.calculate_box(handLm.landmark, image_width, image_height)

            for id, lm in enumerate(handLm.landmark):
                rectangle_top_left = np.minimum(rectangle_top_left, [lm.x * image_width, lm.y * image_height])
                rectangle_bottom_right = np.maximum(rectangle_bottom_right, [lm.x * image_width, lm.y * image_height])
            #     if id not in [0, 1, 5, 6, 9, 10, 13, 14, 17, 18]:
            #         mediapipeHandItem.top_left = np.minimum(mediapipeHandItem.top_left,
            #                                                 [lm.x * image_width, lm.y * image_height])
            #         mediapipeHandItem.bottom_right = np.maximum(mediapipeHandItem.bottom_right,
            #                                                     [lm.x * image_width, lm.y * image_height])

            # Store the center and label of all hands
            hand_center.append(
                (int((rectangle_top_left[0] + rectangle_bottom_right[0]) / 2),
                 int((rectangle_top_left[1] + rectangle_bottom_right[1]) / 2))
            )
        # Add the handedness (left/right)
        for multi_handedness in results.multi_handedness:
            hand_label.append(multi_handedness.classification[0].index)
    return mediapipeHandItem, hand_label, hand_center, no_hands, results.multi_hand_landmarks, frame_mediapipe, rectangle_top_left, rectangle_bottom_right


def yolo_hand_detection(frame):
    width, height, inference_time, results = yolo.inference(frame)
    # sort by confidence
    results.sort(key=lambda x: x[2])

    # how many hands should be shown
    hand_count = len(results)
    x = 0
    y = 0
    w = 0
    h = 0
    # display hands
    for detection in results[:hand_count]:
        id, name, confidence, x, y, w, h = detection
        cx = x + (w / 2)
        cy = y + (h / 2)

        # draw a bounding box rectangle and label on the image
        color = (0, 255, 255)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        text = "%s (%s)" % (name, round(confidence, 2))
        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    color, 2)
    if hand_count != 0:
        hand_is_detected = True
    else:
        hand_is_detected = False
    return hand_is_detected, frame, (x, y), (x + w, y + h)


def thresh_callback(val, src_gray):
    threshold = val
    # Detect edges using Canny
    canny_output = cv2.Canny(src_gray, threshold, threshold * 2)
    # Find contours
    contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Draw contours
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv2.drawContours(drawing, contours, i, color, 2, cv2.LINE_8, hierarchy, 0)
    # Show in a window
    print(contours)
    cv2.imshow('Contours', drawing)


def fast_hand_detection(frame):
    """
    Description: fast hand detection based on paper https://ieeexplore.ieee.org/document/7340956/

    Note: Instead of just choosing the HSV colour space, we have 3 alternatives:
    - HSV
    - YCrCb
    - HSV & YCrCb

    """
    # converting from gbr to hsv color space
    img_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # skin color range for hsv color space
    HSV_mask = cv2.inRange(img_HSV, (0, 15, 0), (17, 170, 255))
    HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    # converting from gbr to YCbCr color space
    img_YCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    # skin color range for hsv color space
    YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255, 180, 135))
    YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    # merge skin detection (YCbCr and hsv)
    global_mask = cv2.bitwise_and(YCrCb_mask, HSV_mask)
    global_mask = cv2.medianBlur(global_mask, 3)
    global_mask = cv2.morphologyEx(global_mask, cv2.MORPH_OPEN, np.ones((4, 4), np.uint8))
    print(YCrCb_mask.shape)
    img_output = algorithm.apply(YCrCb_mask)
    img_bgmodel = algorithm.getBackgroundModel()

    # Then we subtract the background
    frame_fasthand = cv2.bitwise_and(global_mask, img_output)

    # HSV_result = cv2.bitwise_not(HSV_mask)
    # YCrCb_result = cv2.bitwise_not(YCrCb_mask)
    # global_result = cv2.bitwise_not(global_mask)

    # cv2.imshow('img_output', frame_fasthand)
    # cv2.imshow('img_bgmodel', frame_fasthand)
    # dwt2(frame)
    # print("first image ", YCrCb_mask.shape, "second image ", frame.shape)
    # mask = np.ones(frame.shape[:2], np.uint8)
    # mask[100:200, 100:200] = 0
    # cv2.bitwise_and(frame, YCrCb_mask)

    # thresh_callback(50, frame_fasthand)
    n_white_pix = np.sum(frame_fasthand == 255)
    print('Number of white pixels:', n_white_pix)

    return n_white_pix, frame_fasthand


def dwt2(img):
    # convert to grayscale
    imArray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # convert to float
    imArray = np.float32(imArray)
    imArray /= 255
    # compute coefficients
    coeffs2 = pywt.dwt2(imArray, 'bior1.3')
    LL, (LH, HL, HH) = coeffs2
    # Process Coefficients

    cv2.imshow('LL', LL)
    cv2.imshow('LH', LH)
    cv2.imshow('HL', HL)


def bounding_box_diagonal(p1, p2):
    diagonal = math.sqrt(((p1[0] - p2[0]) ** 2) + (
            (p1[1] - p2[1]) ** 2))
    return diagonal


def detect_interaction(p1, p2, threshold):
    diagonal = bounding_box_diagonal(p1, p2)
    # Tuning: yolo_distance = 200, mediapipe_distance = 320
    if diagonal > threshold:
        return True
    else:
        return False
