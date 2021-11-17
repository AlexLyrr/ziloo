import cv2
import mediapipe as mp
import time
import sys

import numpy as np
import matplotlib.pyplot as plt

import pywt
import pywt.data
import pybgs as bgs # This package is manually added


# Open the camera
cap = cv2.VideoCapture(0)
while not cap.isOpened():
    cap = cv2.VideoCapture(0)
    cv2.waitKey(1000)
    print("Wait for the header")
img = []

# Useful mediapipe objects
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Variables for timing measurements
pTime = 0
cTime = 0
fps = 0
minFps = sys.maxsize
maxFps = -sys.maxsize - 1
algorithm = bgs.KNN()

# Function definitions

def mediapipe_hand_detection():
    global img
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLm in results.multi_hand_landmarks:
            for id, lm in enumerate(handLm.landmark):
                mpDraw.draw_landmarks(img, handLm, mpHands.HAND_CONNECTIONS)


def calculate_timings():
    global cTime, pTime, fps, minFps, maxFps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    if fps > maxFps:
        maxFps = fps
    elif fps < minFps:
        minFps = fps


def print_timings():
    print("min fps = " + str(minFps))
    print("max fps = " + str(maxFps))
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)


def w2d(img, mode='haar', level=1):
    # convert to grayscale
    imArray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # convert to float
    imArray = np.float32(imArray)
    imArray /= 255;
    # compute coefficients
    coeffs = pywt.wavedec2(imArray, mode, level=level)

    # Process Coefficients
    coeffs_H = list(coeffs)
    # coeffs_H[0] *= 0;

    # reconstruction
    imArray_H = pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H = np.uint8(imArray_H)
    # Display result
    cv2.imshow('image', imArray_H)


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

    # print("original size = ", img.shape, "LL size = ", LL.shape, "LH size = ", LH.shape)


def fast_hand_detection(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print(hsv_img[0][0])
    # Values according to paper "fast hand detection and gesture recognition"
    low_H = 0
    high_H = 80
    low_S = 25
    high_S = 192
    low_V = 0
    high_V = 255
    # Values according to paper "new hand gesture recognition method for mouse operation"
    # low_H = 0
    # high_H = 20
    # low_S = 30
    # high_S = 150
    # low_V = 80
    # high_V = 255

    hsv_img_threshold = cv2.inRange(hsv_img, (low_H, low_S, low_V), (high_H, high_S, high_V))
    kernel = np.ones((8, 8), np.uint8)
    cv2.morphologyEx(hsv_img_threshold, cv2.MORPH_OPEN, kernel)
    cv2.imshow('hsv_img_threshold_opening', hsv_img_threshold)


def zero_sum_game_theory(img):
    # converting from gbr to hsv color space
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # skin color range for hsv color space
    HSV_mask = cv2.inRange(img_HSV, (0, 15, 0), (17, 170, 255))
    HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    # converting from gbr to YCbCr color space
    img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    # skin color range for hsv color space
    YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255, 180, 135))
    YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    # merge skin detection (YCbCr and hsv)
    global_mask = cv2.bitwise_and(YCrCb_mask, HSV_mask)
    global_mask = cv2.medianBlur(global_mask, 3)
    global_mask = cv2.morphologyEx(global_mask, cv2.MORPH_OPEN, np.ones((4, 4), np.uint8))

    HSV_result = cv2.bitwise_not(HSV_mask)
    YCrCb_result = cv2.bitwise_not(YCrCb_mask)
    global_result = cv2.bitwise_not(global_mask)
    cv2.imshow('hsv_img_threshold_opening', global_mask)


def background_removal(img):
    # Choose one of the two algorithms
    # backSub = cv2.createBackgroundSubtractorMOG2()
    backSub = cv2.createBackgroundSubtractorKNN()
    fgMask = backSub.apply(img)

    # cv2.rectangle(img, (10, 2), (100, 20), (255, 255, 255), -1)
    # cv2.putText(img, str(img.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
    #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    cv2.imshow('Frame', img)
    cv2.imshow('FG Mask', fgMask)

def simple_background_removal(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshold input image as mask
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

    # negate mask
    mask = 255 - mask

    # apply morphology to remove isolated extraneous noise
    # use borderconstant of black since foreground touches the edges
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # anti-alias the mask -- blur then stretch
    # blur alpha channel
    mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=2, sigmaY=2, borderType=cv2.BORDER_DEFAULT)

    # linear stretch so that 127.5 goes to 0, but 255 stays 255
    mask = (2 * (mask.astype(np.float32)) - 255.0).clip(0, 255).astype(np.uint8)

    # put mask into alpha channel
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    # display result, though it won't show transparency
    cv2.imshow("INPUT", img)
    cv2.imshow("GRAY", gray)
    cv2.imshow("MASK", mask)

def background_bgs(frame):
    global cap, pos_frame

    img_output = algorithm.apply(frame)
    img_bgmodel = algorithm.getBackgroundModel()

    cv2.imshow('img_output', img_output)
    cv2.imshow('img_bgmodel', img_bgmodel)


# here we start our program

while True:
    # Read a frame
    pos_frame = cap.get(1)
    success, img = cap.read()

    if not success:
        exit(1)
    # Execute hand detection by mediapipe
    # mediapipe_hand_detection()

    # Calculate and print timings
    calculate_timings()
    print_timings()

    # w2d(img, 'db1', 10)
    # dwt2(img)
    # fast_hand_detection(img)
    # zero_sum_game_theory(img)
    # background_removal(img)
    background_bgs(img)
    # cv2.imshow("Image", img)

    if cv2.waitKey(10) == 27:
        break
