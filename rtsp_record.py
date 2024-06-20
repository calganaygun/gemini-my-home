# Helper for RTSP stream

import cv2
from PIL import Image

def snapshot_rtsp_stream(rtsp_url):
    # Open a connection to the RTSP stream
    cap = cv2.VideoCapture(rtsp_url)
    
    # Check if the connection was successful
    if not cap.isOpened():
        raise Exception(f"Error: Failed to open RTSP stream at {rtsp_url}")

    # Capture a single frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture frame.")
        return

    color_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_converted)

    # Release everything
    cap.release()
    cv2.destroyAllWindows()

    return pil_image