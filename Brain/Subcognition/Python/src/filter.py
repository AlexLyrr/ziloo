import numpy as np

# Average filter dimensions
capacity = 20
average_arr = np.zeros((capacity, 1))


def average_filter(no_hands):
    global average_arr
    average_arr = np.roll(average_arr, 1)
    average_arr[0] = no_hands
    return average_arr.mean()

