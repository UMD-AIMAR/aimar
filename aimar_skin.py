# import cv2
# import matplotlib.pyplot as plt
import io
import time
import picamera
import requests

DESKTOP_URL = "http://10.0.1.5:5000"


# def capture_usbcam():
#     # captures image and stores in 'frame' variable
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     cap.release()
#
#     # save as png buffer
#     buf = io.BytesIO()
#     plt.imsave(buf, frame, format='png')
#     image_data = buf.getvalue()
#     return image_data


def capture_picam():
    # Create an in-memory stream
    buf = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(buf, 'jpeg')
    image_data = buf.getvalue()
    buf.close()
    return image_data


def diagnose_image(image_data):
    resp = requests.post(DESKTOP_URL + "/api/skin", data=image_data)
    return resp.json()