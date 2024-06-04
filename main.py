from app.stream import streaming_camera
from utils.time_stamp import get_time_stamp
from db.controller_db import update_db,delete_db,load_db
from utils.crop_video import crop_video

if __name__ == '__main__':
    #initial clear database
    delete_db()
    option = 'videos/short.mp4'
    streaming_camera(option)
    # streaming_camera(0)
    
    #Load labels from database
    chain_labels = load_db()  
    # Get time stamp
    time_stamp = get_time_stamp(chain_labels,num_tracking=5,num_stop=5)
    
    #Crop video based on time stamp
    for time in time_stamp:
        start_frame = time[0]
        end_frame = time[1]
        cropped_video = crop_video(option, start_frame, end_frame, frame_rate=30)
        cropped_video.write_videofile(f'cropped_{start_frame}_{end_frame}.mp4')
        cropped_video.close()