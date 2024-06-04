
from moviepy.video.io.VideoFileClip import VideoFileClip

def crop_video(video_path, start_frame, end_frame, frame_rate):
    start_time = start_frame / frame_rate
    end_time = end_frame / frame_rate

    video = VideoFileClip(video_path)
    cropped_video = video.subclip(start_time, end_time)

    return cropped_video