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

# Constants
CHAR_ASPECT = 1.5  # Character aspect ratio compensation (width multiplier)

# Get video file first
video_path = find_video_file()
if video_path is None:
    print("Error: No MP4 file found in current directory!")
    exit()

# Get original dimensions
cap = cv2.VideoCapture(video_path)
orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
aspect_ratio = orig_width / orig_height

# Ask for resolution
print(f"Original video resolution: {orig_width}x{orig_height} (aspect ratio: {aspect_ratio:.2f})")

while True:
    try:
        user_input = input("Enter width x height (e.g., '100x100' or '120'): ").strip()
        
        if 'x' in user_input:
            width, height = map(int, user_input.split('x'))
        else:
            height = int(user_input)
            width = int(height * aspect_ratio * CHAR_ASPECT)  # Apply compensation
        
        break
    except ValueError:
        print("Invalid input. Please enter like '100x100' or just '100'")

# Initialize audio after getting dimensions
player = MediaPlayer(video_path)

# ASCII setup
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
    
    # Apply character aspect compensation
    resized_width = int(width * CHAR_ASPECT)
    small = cv2.resize(gray, (resized_width, height))
    
    # Sample to target width
    step = resized_width / width
    ascii_frame = ""
    for row in small:
        sampled_row = [row[int(i*step)] for i in range(width)]
        for pixel in sampled_row:
            index = min(int(pixel / 255 * (len(ascii_chars) - 1)), len(ascii_chars) - 1)
            ascii_frame += ascii_chars[index]
        ascii_frame += "\n"
    
    os.system('clear')
    print(ascii_frame, end='', flush=True)
    
    # Audio sync
    audio_frame, val = player.get_frame()
    if val != 'eof' and audio_frame is not None:
        img, t = audio_frame
    
    frame_count += 1
    sleep_time = target_time - time.time()
    if sleep_time > 0: time.sleep(sleep_time)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
