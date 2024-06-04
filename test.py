from app.stream import streaming_camera
from utils.time_stamp import get_time_stamp
from db.controller_db import update_db,delete_db,load_db
from utils.crop_video import crop_video
import cv2
from utils.detect import load_model, get_label

def test_with_image():
    anchor = cv2.imread('samples/anchor.jpg')
    frame = cv2.imread('samples/0.jpg')
    FM,session = load_model()
    label = get_label(FM, session, anchor, frame)
    print("Result: ", label)
    
def test_with_videos(option):
    delete_db()
    # option = 0
    streaming_camera(option)
    chain_labels = load_db()  
    time_stamp = get_time_stamp(chain_labels,num_tracking=5,num_stop_tracking=5)
    
    #Crop video based on time stamp
    for time in time_stamp:
        start_frame = time[0]
        end_frame = time[1]
        cropped_video = crop_video(option, start_frame, end_frame, frame_rate=30)
        cropped_video.write_videofile(f'cropped_{start_frame}_{end_frame}.mp4')
        cropped_video.close()
        
if __name__ == '__main__':
    # test_with_image()
    test_with_videos('videos/short.mp4')