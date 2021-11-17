import cv2
import numpy as np
import math
from src import filter as fl, hand_detection as hd, gesture_recognizer as gr

# import background as bg


RECTANGLE_EXTENSION_FACTOR = 2
object_counter = 0
is_object_tracked = False


def draw_rectangle(frame_mediapipe, rectangle_top_left_mediapipe, rectangle_bottom_right_mediapipe, image_width,
                   image_height):
    # bounding box parameters
    COLOR = (255, 0, 0)
    THICKNESS = 4

    # rectangle_extension = hd.bounding_box_diagonal(rectangle_top_left_mediapipe,
    #                                                rectangle_bottom_right_mediapipe) / RECTANGLE_EXTENSION_FACTOR
    rectangle_extension = 0
    rectangle_top_left_mediapipe = (np.clip(int(rectangle_top_left_mediapipe[0] - rectangle_extension), 0, image_width),
                                    np.clip(int(rectangle_top_left_mediapipe[1] - rectangle_extension), 0,
                                            image_height))
    rectangle_bottom_right_mediapipe = (
        np.clip(int(rectangle_bottom_right_mediapipe[0] + rectangle_extension), 0, image_width),
        np.clip(int(rectangle_bottom_right_mediapipe[1] + rectangle_extension), 0, image_height))
    frame_mediapipe = cv2.rectangle(frame_mediapipe, rectangle_top_left_mediapipe, rectangle_bottom_right_mediapipe,
                                    COLOR, THICKNESS)


def draw_hand_item_rectangle(frame_mediapipe, hand_label, rectangle_top_left_mediapipe,
                             rectangle_bottom_right_mediapipe, rectangle_extension, image_width, image_height):
    # bounding box parameters
    COLOR = (255, 0, 0)
    THICKNESS = 4

    # No need for extension with current implementation
    rectangle_extension = 0

    ## Hand is right
    if hand_label[0] == 0:
        rectangle_top_left_mediapipe = (
            np.clip(int(rectangle_top_left_mediapipe[0]), 0, image_width),
            np.clip(int(rectangle_top_left_mediapipe[1]), 0,
                    image_height))
        rectangle_bottom_right_mediapipe = (np.clip(int(rectangle_bottom_right_mediapipe[0] + rectangle_extension), 0,
                                                    image_width),
                                            np.clip(int(rectangle_bottom_right_mediapipe[1]), 0, image_height))
    elif hand_label[0] == 1:
        rectangle_top_left_mediapipe = (
            np.clip(int(rectangle_top_left_mediapipe[0] - rectangle_extension), 0, image_width),
            np.clip(int(rectangle_top_left_mediapipe[1]), 0,
                    image_height))
        rectangle_bottom_right_mediapipe = (np.clip(int(rectangle_bottom_right_mediapipe[0]), 0,
                                                    image_width),
                                            np.clip(int(rectangle_bottom_right_mediapipe[1]), 0, image_height))

    cv2.rectangle(frame_mediapipe, rectangle_top_left_mediapipe, rectangle_bottom_right_mediapipe,
                  COLOR, THICKNESS)
    # cv2.imshow("background removal", bg.background_removal(frame_mediapipe))


def calculate_dist(p1, p2):
    dist = math.sqrt(((p1[0] - p2[0]) ** 2) + (
            (p1[1] - p2[1]) ** 2))
    return dist


def process(face_detections, mediapipeHandItem, hand_label, hand_center, no_hands, image_height, image_width,
                           multi_hand_landmarks, frame, frame_mediapipe, rectangle_top_left_mediapipe,
                           rectangle_bottom_right_mediapipe):
    global object_counter, is_object_tracked
    is_object_hold = False

    # Filter number of hands based on distance between centers
    i = 1
    while i < len(hand_center):
        if calculate_dist(hand_center[i - 1], hand_center[i]) < 100:
            no_hands -= 1
            hand_center.pop(i)
        else:
            i += 1
    # Low pass filter the number of hands to smooth the output
    no_hands_filtered = fl.average_filter(no_hands)
    # Draw the center of the hands
    if (no_hands > 0):
        for i in range(no_hands):
            cv2.circle(frame_mediapipe, hand_center[i], 2, (255, 255, 0), -1)
    if multi_hand_landmarks:
        # convert array to point
        is_interaction_intended = hd.detect_interaction(rectangle_bottom_right_mediapipe, rectangle_top_left_mediapipe,
                                                        300)
        if is_interaction_intended:
            cv2.putText(frame_mediapipe, "Interaction", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 2)
        # cv2.imshow("Hand", frame[rectangle_top_left_mediapipe[1]:rectangle_bottom_right_mediapipe[1], rectangle_top_left_mediapipe[0]:rectangle_bottom_right_mediapipe[0]])
        # sg.segment_KNN(frame[rectangle_top_left_mediapipe[1]:rectangle_bottom_right_mediapipe[1], rectangle_top_left_mediapipe[0]:rectangle_bottom_right_mediapipe[0]])
        # sg.segment_contour(frame[rectangle_top_left_mediapipe[1]:rectangle_bottom_right_mediapipe[1], rectangle_top_left_mediapipe[0]:rectangle_bottom_right_mediapipe[0]])
        # sg.segment_hand_colour_threshold(frame_mediapipe[mediapipeHandItem.top_left[1]:mediapipeHandItem.bottom_right[1], mediapipeHandItem.top_left[0]:mediapipeHandItem.bottom_right[0]])
        # sg.remove_hand(
        #     frame_mediapipe[mediapipeHandItem.top_left[1]:mediapipeHandItem.bottom_right[1],
        #     mediapipeHandItem.top_left[0]:mediapipeHandItem.bottom_right[0]])

        # gesture = gr.hand_gesture_recognition(multi_hand_landmarks)
        # cv2.putText(frame_mediapipe, gesture, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 50, 150), 3)
        is_object_hold = gr.is_object_hold(multi_hand_landmarks, is_interaction_intended)
        # is_object_hold = True
        if is_object_hold:
            # Draw the hand rectangle
            extension = hd.bounding_box_diagonal(rectangle_top_left_mediapipe,
                                                 rectangle_bottom_right_mediapipe) / RECTANGLE_EXTENSION_FACTOR
            draw_hand_item_rectangle(frame_mediapipe, hand_label, mediapipeHandItem.top_left,
                                     mediapipeHandItem.bottom_right, extension,
                                     image_width, image_height)
            cv2.putText(frame_mediapipe, "HOLD", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 50, 150), 3)
    # cv2.putText(frame_mediapipe, str(no_hands), (10, 130), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)
    cv2.putText(frame_mediapipe, "Hands = " + str(int(no_hands_filtered)), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    if no_hands_filtered > 0 and is_object_hold and not is_object_tracked:
        object_counter += 1
        is_object_tracked = True
    if no_hands_filtered == 0:
        is_object_tracked = False
    cv2.putText(frame_mediapipe, "Objects = " + str(int(object_counter)), (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 0, 255), 2)

    # Is object seen?
    # draw_num_hands(no_hands_filtered, frame_mediapipe)

    return is_object_hold


def capture_detected_object():
    pass
