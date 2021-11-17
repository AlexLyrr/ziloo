import time
import sys

#####################
##### VARIABLES #####
#####################

g_sTime = 0
g_eTime = 0
g_func_name = ""
g_min_fps = {"mediapipe": sys.maxsize}
g_max_fps = {"mediapipe": -sys.maxsize - 1}
g_total_fps = 0
g_total_hits = 0
g_total_exec_time = 0

#####################
##### FUNCTIONS #####
#####################

# start profiling the function
def start_profiling(func_name):
    global g_sTime, g_eTime, g_func_name
    g_sTime = time.time()
    g_func_name = func_name

# finish profiling the function
def finish_profiling(multi_hand_landmarks):
    global g_sTime, g_eTime, g_func_name, g_min_fps, g_max_fps, g_total_fps, g_total_hits, g_total_exec_time
    g_eTime = time.time()
    exec_time = g_eTime - g_sTime
    g_fps = 1 / exec_time
    if g_fps < g_min_fps["mediapipe"]:
        g_min_fps["mediapipe"] = g_fps
    elif g_fps > g_max_fps["mediapipe"]:
        g_max_fps["mediapipe"] = g_fps
    print("-- [{}] Execution time of ".format(__name__) + g_func_name + " = " + str(g_fps) + " FPS")
    if True:
        g_total_exec_time += exec_time
        g_total_fps += g_fps
        g_total_hits += 1

# print the average execution time of the function when program exits
def print_average():
    global g_total_hits
    if g_total_hits is not 0:
        print("Average exec time = " + str(float(g_total_exec_time) / g_total_hits) + "\nTotal hits = " + str(g_total_hits))
        print("Average FPS = " + str(float(g_total_fps)/g_total_hits) + "\nTotal hits = " + str(g_total_hits))
        print("Total hits = " + str(g_total_hits))
    else:
        print("No hits in this sample")
