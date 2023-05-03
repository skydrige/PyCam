import cv2

# Open the video file
video_capture = cv2.VideoCapture('camera1_2023-05-02_23-53-40.avi')

# Check if the video file is opened successfully
if not video_capture.isOpened():
    print("Error: Could not open video file")
    exit()

# Read the frames of the video file and display them
while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    cv2.imshow('Video', frame)
    
    # Wait for 25 milliseconds and check if the user has pressed 'q' to quit
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# Release the video file and close the window
video_capture.release()
cv2.destroyAllWindows()
