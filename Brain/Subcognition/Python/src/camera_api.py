import cv2
import time

cap = None
writer = None
width = 0
height = 0


# Open the camera
def open_camera():
    global cap, width, height
    cap = cv2.VideoCapture(0)
    while not cap.isOpened():
        cap = cv2.VideoCapture(0)
        cv2.waitKey(1000)
        print("-- [{}] Wait for the header".format(__name__))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("-- [{}] Camera successfully opened".format(__name__))

# Open the writer
def open_writer(output):
    global writer
    writer = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

# Open the video
def open_video(video_name):
    global cap, width, height
    cap = cv2.VideoCapture(video_name)
    if not cap.isOpened():
        print("-- [{}] Video not found".format(__name__))
        exit(1)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("-- [{}] Video successfully opened".format(__name__))

# Close the camera
def close_camera():
    global cap
    cap.release()
    cv2.destroyAllWindows()

# Get a frame
def get_frame():
    success, frame = cap.read()
    return success, frame

# Write a frame
def write_frame(frame):
    writer.write(frame)

# Record video for <secs> seconds
def record(secs):
    frame = get_frame()
    writer = cv2.VideoWriter('subcognition_sample_1.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width, height))
    start = time.time()
    now = time.time()
    time.sleep(5)
    print("##START RECORDING##")
    while (now - start <  secs):
        cv2.imshow("video", frame)
        writer.write(frame)
        frame = get_frame()
        now = time.time()
    print("##FINISH RECORDING##")
    writer.release()
