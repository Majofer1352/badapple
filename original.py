import os
import cv2
import time
import numpy as np
from ffpyplayer.player import MediaPlayer

def find_video_file():
    for file in os.listdir('.'):
        if file.lower().endswith('.mp4'):
            return file
    return None

# Get video file
video_path = find_video_file()
if video_path is None:
    print("Error: No MP4 file found in current directory!")
    exit()

cap = cv2.VideoCapture(video_path)
player = MediaPlayer(video_path)

# Get original dimensions
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# ASCII characters
ascii_chars = " .,:;+*?%S#@"
fps = cap.get(cv2.CAP_PROP_FPS)
frame_delay = 1.0 / fps

start_time = time.time()
frame_count = 0

while cap.isOpened():
    target_time = start_time + (frame_count * frame_delay)
    ret, frame = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (width, height))
    
    ascii_frame = ""
    for row in small:
        for pixel in row:
            index = min(int(pixel / 255 * (len(ascii_chars) - 1)), len(ascii_chars) - 1)
            ascii_frame += ascii_chars[index]
        ascii_frame += "\n"
    
    os.system('clear')
    print(ascii_frame, end='', flush=True)
    
    audio_frame, val = player.get_frame()
    if val != 'eof' and audio_frame is not None:
        img, t = audio_frame
    
    frame_count += 1
    sleep_time = target_time - time.time()
    if sleep_time > 0: time.sleep(sleep_time)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
