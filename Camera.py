from flask import Flask, Response, redirect, request, jsonify, render_template, url_for
import cv2
import datetime
import time
import os
import threading


app = Flask(__name__)

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use 0 to access the default camera

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error opening the camera")
    exit()


def generate_frames():
    """Generate camera frames as a response to a GET request."""
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame is captured successfully
        if not ret:
            print("Error capturing the frame")
            break

        # Convert the frame to a JPEG image
        _, jpeg = cv2.imencode('.jpg', frame)

        # Yield the JPEG image as a byte stream
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


class Camera:
    """A camera class to hold camera information and control recording."""

    def __init__(self, camera_id, location):
        self.camera_id = camera_id
        self.location = location
        self.recording = False

    def start_recording(self, duration):
        """Start recording for the camera for specified duration."""
        if self.recording:
            print(f'Camera {self.camera_id} is already recording.')
            return

        self.recording = True
        print(f'Recording started for camera {self.camera_id} for {duration} seconds at {datetime.datetime.now()}.')

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        filename = f'camera{self.camera_id}_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.avi'
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

        # Write frames to video file for the duration of the recording
        start_time = time.time()
        while time.time() - start_time < duration:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Check if the frame is captured successfully
            if not ret:
                print("Error capturing the frame")
                break

            # Write the frame to the video file
            out.write(frame)

        # Release the VideoWriter object and stop recording
        out.release()
        self.stop_recording()

    def stop_recording(self):
        """Stop recording for the camera."""
        if not self.recording:
            print(f'Camera {self.camera_id} is not recording.')
            return

        self.recording = False
        print(f'Recording stopped for camera {self.camera_id} at {datetime.datetime.now()}.')



# create camera objects and add to dictionary
cameras = {}
cameras['camera1'] = Camera(camera_id=1, location='D13')


@app.route('/')
def index():
    """Render the video stream in a HTML page."""
    return (
        f'<html>'
        f'<head><title>Camera Stream</title></head>'
        f'<body><h1>Camera Stream</h1>'
        f'<img src="/video_feed">'
        f'<br><br>'
        f'<form action="/record_camera" method="POST">'
        f'<label for="camera_id">Select a camera:</label>'
        f'<select name="camera_id" id="camera_id">'
        f'<option value="camera1">Camera 1 - D13</option>'
        f'</select>'
        f'<br><br>'
        f'<label for="duration">Recording duration (in seconds):</label>'
        f'<input type="number" name="duration" id="duration" value="10" required>'
        f'<br><br>'
        f'<input type="submit" value="Record" class="submit">'
        f'</form>'
        f'</body></html>'
    )


@app.route('/video_feed')
def video_feed():
    """Stream the camera frames as a response to a GET request."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/record_camera', methods=['POST'])
def start_camera_recording():
    camera_id = request.form['camera_id']
    duration = int(request.form['duration'])

    # Start recording for camera
    cameras[camera_id].start_recording(duration)

    # Redirect back to index page
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Start the web server on port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
