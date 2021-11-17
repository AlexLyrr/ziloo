import cv2
from src import profiler as prof, hand_detection as hd, face_detection as fd, post_img_processor as pp, \
    camera_api as cam, classifier as cf
import argparse

ap = argparse.ArgumentParser(description='Detect the surroundings and user interactions')
ap.add_argument('-n',
                '--network',
                default="mediapipe",
                help='Network Type: mediapipe|yolo|fast')
ap.add_argument('-cl',
                '--classifier',
                default="efficientnetb0",
                help='Classifier Type: resnet50|mobilenetv2|efficientnetb0')

args = ap.parse_args()
# args.network = "mediapipe"
# args.classifier = "efficientnetb0"

print(args.network, "algorithm selected")

# test parameters
INPUT = 1 # 0: Camera, 1: Video
PROFILE = True # if false, then we don't profile execution
CONVERT_LOWER_FPS = True # if true, then we discard frames. If false, FPS = 30 (camera frame rate)
# FRAMES_TO_DROP = 14 # FPS = 2
# FRAMES_TO_DROP = 5 # FPS = 5
FRAMES_TO_DROP = 1 # FPS = 15
RECORD = True
CLASSIFY = True

sample_name = "sample-6.mkv"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Welcome to the Subcognition application')
### STAGE 1: SYSTEM INITIALIZATION
    # Open the camera or video sample
    if INPUT == 0:
        cam.open_camera()
    elif INPUT == 1:
        cam.open_video('/home/alyr/subcognition/video/' + sample_name)
    # Initialize the video recorder
    if RECORD:
        cam.open_writer('/home/alyr/subcognition/video/' + sample_name + '_' + args.network + '_' + args.classifier + '.mp4')
    elif CONVERT_LOWER_FPS:
        cam.open_writer('/home/alyr/subcognition/video/' + sample_name + '-lowerfps_' + args.network +'.mp4')
    else:
        cam.open_writer('/home/alyr/subcognition/video/' + sample_name + '_' + args.network + '.mp4')
    while True:
# STAGE 2: PREPROCESSING
# No preprocessing is performed so far
# STAGE 3: PROCESSING
        success, frame = cam.get_frame()
        if not success:
            break
        image_height, image_width, _ = frame.shape
        ## HAND DETECTION
        ### Mediapipe detection
        if args.network == "mediapipe":
            # if PROFILE:
            #     prof.start_profiling("mediapipe")
            # Run the mediapipe hand detection
            mediapipeHandItem, hand_label, hand_center, no_hands, multi_hand_landmarks, frame_processed, rectangle_top_left_mediapipe, rectangle_bottom_right_mediapipe = hd.mediapipe_hand_detection(frame)
            # if PROFILE:
            #     prof.finish_profiling(multi_hand_landmarks)
        ### Yolo detection
        elif args.network == "yolo":
            # if PROFILE:
            #     prof.start_profiling("yolo")
            hand_is_detected_yolo, frame_processed, rectangle_top_left_yolo, rectangle_bottom_right_yolo = hd.yolo_hand_detection(frame)
            # if PROFILE:
            #     prof.finish_profiling()
        ### Fast hand detection
        elif args.network == "fast":
            # if PROFILE:
            #     prof.start_profiling("fast hand detection")
            n_white_pix, frame_processed = hd.fast_hand_detection(frame)
            # if PROFILE:
            #     prof.finish_profiling()
            cv2.putText(frame, "#white pixels = " + str(n_white_pix), (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 200), 3)
            if n_white_pix > 17000:
                cv2.putText(frame, "Interaction", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        ## FACE DETECTION
        if PROFILE:
            prof.start_profiling("mediapipe face detection")
        frame_processed, face_detections = fd.face_detection_mediapipe(frame_processed)
        if PROFILE:
            prof.finish_profiling(face_detections)
# STAGE 3: POST-PROCESSING
        if args.network == "mediapipe":
            is_object_hold = pp.process(face_detections, mediapipeHandItem, hand_label, hand_center, no_hands, image_height, image_width, multi_hand_landmarks, frame, frame_processed,
                                                       rectangle_top_left_mediapipe, rectangle_bottom_right_mediapipe)
            if is_object_hold:
                frame_object = frame[mediapipeHandItem.top_left[1]:mediapipeHandItem.bottom_right[1],
                                         mediapipeHandItem.top_left[0]:mediapipeHandItem.bottom_right[0]]

                cv2.imshow("object detected", frame_object)
                ## CLASSIFY THE DETECTED OBJECT
                if CLASSIFY:
                    preds = cf.model_predict(frame_object, cf.model)

                    # Process your result for human

                    pred_class = cf.decode_predictions(preds, top=5)  # ImageNet Decode
                    result = "{} score: {}, {} score: {}, {} score: {}, {} score: {}, {} score: {}".format(str(pred_class[0][0][1]), str(pred_class[0][0][2]), str(pred_class[0][1][1]), str(pred_class[0][1][2]), str(pred_class[0][2][1]), str(pred_class[0][2][2]),  str(pred_class[0][3][1]), str(pred_class[0][3][2]), str(pred_class[0][4][1]), str(pred_class[0][4][2]))
                    for substring in ["lighter", "mouse", "control", "bottle", "sunglass", "telephone", "cap"]:
                        if substring in result:
                            cv2.putText(frame_processed, substring, (300, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 150, 255), 2)
                    print(result)
                    result = str(pred_class[0][0][1])  # Convert to string

# STAGE 4: OUTPUT
        cv2.imshow("Frame processed", frame_processed)
        cam.write_frame(frame_processed)

        if cv2.waitKey(2) == 27:
            break
        if CONVERT_LOWER_FPS:
            for x in range(FRAMES_TO_DROP):
                frame = cam.get_frame()
    prof.print_average()


