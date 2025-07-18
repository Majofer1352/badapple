import os
import cv2
import time
import numpy as np
from ffpyplayer.player import MediaPlayer

# Find first MP4 file in current directory
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

# Get video FPS and calculate frame delay
fps = cap.get(cv2.CAP_PROP_FPS)
frame_delay = 1.0 / fps

# Terminal dimensions and ASCII characters
width, height = 220, 109
ascii_chars = " .,:;+*?%S#@"

# Start playback
start_time = time.time()
frame_count = 0

while cap.isOpened():
    # Calculate exact time when this frame should be displayed
    target_time = start_time + (frame_count * frame_delay)
    
    # Read video frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Process frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (width, height))
    
    # Convert to ASCII
    normalized = small / 255.0
    ascii_frame = ""
    for row in normalized:
        for val in row:
            index = min(int(val * (len(ascii_chars) - 1)), len(ascii_chars) - 1)
            ascii_frame += ascii_chars[index]
        ascii_frame += "\n"
    
    # Display
    os.system('clear')
    print(ascii_frame, end='', flush=True)
    
    # Audio sync (check but don't block)
    audio_frame, val = player.get_frame()
    if val != 'eof' and audio_frame is not None:
        img, t = audio_frame
    
    # Maintain frame timing
    frame_count += 1
    sleep_time = target_time - time.time()
    if sleep_time > 0:
        time.sleep(sleep_time)
    
    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
