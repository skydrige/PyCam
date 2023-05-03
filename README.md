# Camera Streaming and Recording using Flask

This is a simple Flask app that streams video frames from the camera and allows users to record a video from a selected camera.

## Dependencies
- Python 3
- Flask
- OpenCV

## Usage
1. Install dependencies by running `pip install -r requirements.txt`.
2. Run the app using `python Camera.py`.
3. Open a web browser and navigate to `http://localhost:8080`.
4. The camera stream should be visible on the page.
5. Select a camera and recording duration, then click the "Record" button to start recording.
6. The recorded video will be saved to disk.

## Code Structure
- `Camera.py`: Contains the Flask app code.

# Video Streaming using OpenCV

This is a Python script that reads frames from a video file and displays them in a window using OpenCV.

## Dependencies

- Python 3
- OpenCV

## Usage

1. Install OpenCV by running `pip install opencv-python`.
2. Save your video file in the same directory as the Python script.
3. Update the file name in `cv2.VideoCapture()` to match your video file.
4. Run the script using `python ViewCam.py`.
5. The video should start playing in a window.
6. Press 'q' to quit the window and stop the video.

## Code Structure

- `ViewCam.py`: Contains the Python script code.

## Acknowledgements
This project was inspired by the [Camera Streaming and Recording using Flask and OpenCV](https://github.com/skydrige/PyCam) example by [Skydrige](https://github.com/skydrige).
