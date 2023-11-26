import cv2

def load_video(video_path):
    try:
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise Exception(f"Unable to open video file: {video_path}")
        return video
    except:
        return None