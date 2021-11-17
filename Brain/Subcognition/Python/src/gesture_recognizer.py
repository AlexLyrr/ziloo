import cv2
import numpy as np
from math import dist

CLOSENESS_THRESH = 0.08


def hand_gesture_recognition(multi_hand_landmarks):
    thumbIsOpen = False
    firstFingerIsOpen = False
    secondFingerIsOpen = False
    thirdFingerIsOpen = False
    fourthFingerIsOpen = False

    thumbIsOpen = is_thumb_open(multi_hand_landmarks, thumbIsOpen)
    firstFingerIsOpen = is_firstfinger_open(multi_hand_landmarks, firstFingerIsOpen)
    secondFingerIsOpen = is_secondfinger_open(multi_hand_landmarks, secondFingerIsOpen)
    thirdFingerIsOpen = is_thirdfinger_open(multi_hand_landmarks, thirdFingerIsOpen)
    fourthFingerIsOpen = is_fourthfinger_open(multi_hand_landmarks, fourthFingerIsOpen)
    print("firstFinger = ", firstFingerIsOpen, "secondFinger = ", secondFingerIsOpen, "secondFinger = ",
          thirdFingerIsOpen, "thirdFinger = ", fourthFingerIsOpen, "thumb = ", thumbIsOpen)
    return get_hand_gesture(multi_hand_landmarks, thumbIsOpen, firstFingerIsOpen, secondFingerIsOpen, thirdFingerIsOpen,
                            fourthFingerIsOpen)


def is_object_hold(multi_hand_landmarks, is_interaction_intended):
    # print(abs(multi_hand_landmarks[0].landmark[6].y - multi_hand_landmarks[0].landmark[7].y),
    #       abs(multi_hand_landmarks[0].landmark[6].y - multi_hand_landmarks[0].landmark[8].y),
    #       abs(multi_hand_landmarks[0].landmark[6].y - multi_hand_landmarks[0].landmark[10].y))
    if (is_interaction_intended and
            (abs(multi_hand_landmarks[0].landmark[6].y - multi_hand_landmarks[0].landmark[7].y) < CLOSENESS_THRESH) and
            (abs(multi_hand_landmarks[0].landmark[6].y - multi_hand_landmarks[0].landmark[8].y) < CLOSENESS_THRESH) and
            (abs(multi_hand_landmarks[0].landmark[6].y - multi_hand_landmarks[0].landmark[10].y) < CLOSENESS_THRESH) and
            (abs(multi_hand_landmarks[0].landmark[6].y - multi_hand_landmarks[0].landmark[12].y) < CLOSENESS_THRESH) and
            (abs(multi_hand_landmarks[0].landmark[6].y - multi_hand_landmarks[0].landmark[16].y) < CLOSENESS_THRESH) and
            (abs(
                multi_hand_landmarks[0].landmark[10].y - multi_hand_landmarks[0].landmark[11].y) < CLOSENESS_THRESH) and
            (abs(
                multi_hand_landmarks[0].landmark[10].y - multi_hand_landmarks[0].landmark[12].y) < CLOSENESS_THRESH) and
            (abs(
                multi_hand_landmarks[0].landmark[10].y - multi_hand_landmarks[0].landmark[14].y) < CLOSENESS_THRESH) and
            (abs(
                multi_hand_landmarks[0].landmark[14].y - multi_hand_landmarks[0].landmark[15].y) < CLOSENESS_THRESH) and
            (abs(
                multi_hand_landmarks[0].landmark[14].y - multi_hand_landmarks[0].landmark[16].y) < CLOSENESS_THRESH) and
            (abs(multi_hand_landmarks[0].landmark[14].y - multi_hand_landmarks[0].landmark[6].y) < CLOSENESS_THRESH)):
        return True
    return False


def is_thumb_open(multi_hand_landmarks, thumbIsOpen):
    pseudoFixKeyPoint = multi_hand_landmarks[0].landmark[2].x
    if (multi_hand_landmarks[0].landmark[3].x < pseudoFixKeyPoint and
            multi_hand_landmarks[0].landmark[4].x < pseudoFixKeyPoint):
        thumbIsOpen = True
    return thumbIsOpen


def is_firstfinger_open(multi_hand_landmarks, firstFingerIsOpen):
    pseudoFixKeyPoint = multi_hand_landmarks[0].landmark[6].y
    if (multi_hand_landmarks[0].landmark[7].y < pseudoFixKeyPoint and
            multi_hand_landmarks[0].landmark[8].y < pseudoFixKeyPoint):
        firstFingerIsOpen = True
    return firstFingerIsOpen


def is_secondfinger_open(multi_hand_landmarks, secondFingerIsOpen):
    pseudoFixKeyPoint = multi_hand_landmarks[0].landmark[10].y
    if (multi_hand_landmarks[0].landmark[11].y < pseudoFixKeyPoint and
            multi_hand_landmarks[0].landmark[12].y < pseudoFixKeyPoint):
        secondFingerIsOpen = True
    return secondFingerIsOpen


def is_thirdfinger_open(multi_hand_landmarks, thirdFingerIsOpen):
    pseudoFixKeyPoint = multi_hand_landmarks[0].landmark[14].y
    if (multi_hand_landmarks[0].landmark[15].y < pseudoFixKeyPoint and
            multi_hand_landmarks[0].landmark[16].y < pseudoFixKeyPoint):
        thirdFingerIsOpen = True
    return thirdFingerIsOpen


def is_fourthfinger_open(multi_hand_landmarks, fourthFingerIsOpen):
    pseudoFixKeyPoint = multi_hand_landmarks[0].landmark[18].y
    if (multi_hand_landmarks[0].landmark[19].y < pseudoFixKeyPoint and
            multi_hand_landmarks[0].landmark[20].y < pseudoFixKeyPoint):
        fourthFingerIsOpen = True
    return fourthFingerIsOpen


def isThumbNearFirstFinger(point1, point2):
    distance = np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
    return distance < 0.1;


def get_hand_gesture(multi_hand_landmarks, thumbIsOpen, firstFingerIsOpen, secondFingerIsOpen, thirdFingerIsOpen,
                     fourthFingerIsOpen):
    if thumbIsOpen and firstFingerIsOpen and secondFingerIsOpen and thirdFingerIsOpen and fourthFingerIsOpen:
        # print("FIVE!")
        return "FIVE!"
    elif (not thumbIsOpen) and firstFingerIsOpen and secondFingerIsOpen and thirdFingerIsOpen and fourthFingerIsOpen:
        # print("FOUR!")
        return "FOUR!"
    elif thumbIsOpen and firstFingerIsOpen and secondFingerIsOpen and not thirdFingerIsOpen and not fourthFingerIsOpen:
        # print("THREE!")
        return "THREE!"
    elif thumbIsOpen and firstFingerIsOpen and (not secondFingerIsOpen) and (not thirdFingerIsOpen) and (
            not fourthFingerIsOpen):
        # print("TWO!")
        return "TWO!"
    elif (not thumbIsOpen) and firstFingerIsOpen and (not secondFingerIsOpen) and (not thirdFingerIsOpen) and (
            not fourthFingerIsOpen):
        # print("ONE")
        return "ONE!"
    elif (not thumbIsOpen) and firstFingerIsOpen and secondFingerIsOpen and (not thirdFingerIsOpen) and (
            not fourthFingerIsOpen):
        # print("YEAH")
        return "YEAH"
    elif (not thumbIsOpen) and firstFingerIsOpen and (not secondFingerIsOpen) and (
            not thirdFingerIsOpen) and fourthFingerIsOpen:
        # print("ROCK")
        return "ROCK"
    elif thumbIsOpen and firstFingerIsOpen and (not secondFingerIsOpen) and (
            not thirdFingerIsOpen) and fourthFingerIsOpen:
        print("Spiderman")
        return "Spiderman"
    elif (not thumbIsOpen) and (not firstFingerIsOpen) and (not secondFingerIsOpen) and (not thirdFingerIsOpen) and (
            not fourthFingerIsOpen):
        # print("FIST")
        return "FIST"
    elif (not firstFingerIsOpen) and secondFingerIsOpen and thirdFingerIsOpen and fourthFingerIsOpen and \
            isThumbNearFirstFinger(multi_hand_landmarks[0].landmark[4], multi_hand_landmarks[0].landmark[8]):
        # print("OK")
        return "OK"
    else:
        # print("Gesture not recognised")
        return "Gesture not recognised"
