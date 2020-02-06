import cv2
import io
import matplotlib.pyplot as plt
import requests

DESKTOP_URL = "http://localhost:5000"


def capture_photo_and_diagnose():
    # captures image and stores in 'frame' variable
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    # save as png buffer
    buf = io.BytesIO()
    plt.imsave(buf, frame, format='png')
    image_data = buf.getvalue()

    # send to desk-server
    resp = requests.post(DESKTOP_URL + "/api/skin", data=image_data)
    return resp.json()
