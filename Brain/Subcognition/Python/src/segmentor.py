import cv2
import numpy as np


def segment_KNN(frame):
    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    twoDimage = frame_RGB.reshape((-1, 3))
    twoDimage = np.float32(twoDimage)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 2
    attempts = 10
    ret, label, center = cv2.kmeans(twoDimage, K, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    result_image = res.reshape((frame.shape))
    label = label.flatten()
    masked_image = np.copy(frame_RGB)
    masked_image = masked_image.reshape((-1, 3))
    cluster = 1
    masked_image[label == cluster] = [0, 0, 0]
    masked_image = masked_image.reshape(frame_RGB.shape)
    # cv2.imshow('KNN', result_image)
    cv2.imshow('KNN', masked_image)


def segment_contour(frame):
    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame_RGB, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, np.mean(gray), 255, cv2.THRESH_BINARY_INV)
    edges = cv2.dilate(cv2.Canny(thresh, 0, 255), None)
    cnt = sorted(cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2], key=cv2.contourArea)[-1]
    mask = np.zeros(frame.shape[:2], np.uint8)
    masked = cv2.drawContours(mask, [cnt], -1, 255, -1)
    dst = cv2.bitwise_and(frame, frame, mask=mask)
    segmented = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    cv2.imshow('Contour with Canny detector', segmented)
    return segmented


def segment_hand_colour_threshold(frame):
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

    mask = cv2.bitwise_or(YCrCb_mask, HSV_mask)
    mask3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # 3 channel mask
    segmented = cv2.bitwise_and(frame, mask3)
    cv2.imshow('Colour segmentation', segmented)

def remove_hand(frame):
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

    mask = cv2.bitwise_or(YCrCb_mask, HSV_mask)
    mask3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # 3 channel mask

    mask3 = cv2.bitwise_not(mask3)
    segmented = cv2.bitwise_and(frame, mask3)
    frame = cv2.bitwise_and(frame, mask3)

    cv2.imshow('Colour segmentation', segmented)
    return segmented

def filter_mask(frame, mask):
    frame = cv2.bitwise_and(frame, mask)
