import re

def load_labels():
    pass

def get_time_stamp(chain_labels:str, num_tracking:int = 5, num_stop_tracking:int = 5):
    """
    Get the time stamps for tracking based on chain labels.

    Args:
        chain_labels (str): The chain labels indicating normal (1) or abnormal (0) behavior.
        num_tracking (int): The minimum number of consecutive frames to consider as a valid tracking.
        num_stop_tracking (int): The maximum number of normal frames to stop tracking.

    Returns:
        list: A list of tuples representing the start and end indices of valid tracking time stamps.
    """
    time_stamp = []
    track_out_abnormal = 0
    start = None
    for idx,label in enumerate(chain_labels):
        if (label == '0'):
            if  (start == None): # discover abnormal -> start tracking
                start = idx
        else:
            track_out_abnormal += 1
            if track_out_abnormal >= num_stop_tracking:
                if start is not None:
                    len_frame_tracking = idx - track_out_abnormal - start
                    if len_frame_tracking >= num_tracking:
                        time_stamp.append((start,idx-track_out_abnormal))
                    start = None
                track_out_abnormal = 0
    return time_stamp
