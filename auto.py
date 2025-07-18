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

# Pobierz oryginalne wymiary
orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
aspect_ratio = orig_width / orig_height

# Ścisłe limity
MAX_HEIGHT = 200
MAX_CHARS = 25000
CHAR_ASPECT = 2.0  # Współczynnik proporcji znaków terminala (~2:1 wysokość:szerokość)

# Oblicz wymiary z kompensacją proporcji znaków
def calculate_dimensions():
    # Skorygowany współczynnik proporcji
    adjusted_ratio = aspect_ratio * CHAR_ASPECT
    
    height = min(orig_height, MAX_HEIGHT)
    width = int(height * adjusted_ratio)
    
    if (width * (height + 1)) > MAX_CHARS:
        max_width = int((MAX_CHARS / (height + 1)))
        height = int(max_width / adjusted_ratio)
        width = int(height * adjusted_ratio)
        
        if height > MAX_HEIGHT:
            height = MAX_HEIGHT
            width = int(height * adjusted_ratio)
    
    return width, height

width, height = calculate_dimensions()
width, height = max(1, width), max(1, height)

# Znaki ASCII
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
    
    # Przeskalowanie z kompensacją proporcji znaków
    resized_width = int(width * CHAR_ASPECT)
    small = cv2.resize(gray, (resized_width, height))
    
    # Próbkowanie do docelowej szerokości
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
    
    audio_frame, val = player.get_frame()
    if val != 'eof' and audio_frame is not None:
        img, t = audio_frame
    
    frame_count += 1
    sleep_time = target_time - time.time()
    if sleep_time > 0: time.sleep(sleep_time)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
