# Bad Apple!! ASCII Animation

A Python script that plays the Bad Apple!! video as ASCII art in your terminal with synchronized audio.

![Bad Apple ASCII Demo](demo.gif) *(example gif would go here)*

## Requirements

- Python 3.6+
- FFmpeg
- Linux/macOS terminal (Windows may need adjustments)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Majofer1352/badapple
cd badapple
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install opencv-python ffpyplayer numpy
```

4. (Optional) For better performance:
```bash
sudo apt-get install ffmpeg  # On Ubuntu/Debian
```

## Usage

1. Place your `badapple.mp4` file in the project directory
2. Run the script:
```bash
python3 audio.py
```
