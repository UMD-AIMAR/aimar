import cv2
import io
import time
import requests
import yaml

picamera_enabled = False

try:
    import picamera
    picamera_enabled = True
except ImportError as ex:
    print(f"No picamera library found. Picamera functions will not be usable.")

try:
    with open("config.yml", "r") as config_data:
        CONFIG = yaml.load(config_data, Loader=yaml.BaseLoader)
        DESKTOP_IP = CONFIG["DESKTOP_IP"]
except IOError:
    print("config.yml does not exist! Generating default config.yml...")
    d = {"DESKTOP_IP": "127.0.0.1"}
    file = open("config.yml", "w")
    file.write(yaml.dump(d))
    exit()


def capture_usbcam():
    # captures image and stores in 'frame' variable
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    # save as png buffer
    is_success, arr = cv2.imencode(".jpg", frame)
    buf = io.BytesIO(arr)
    image_data = buf.getvalue()
    return image_data


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


def diagnose_image(image_data=None):
    try:
        if image_data is None:
            if picamera_enabled:
                image_data = capture_picam()
            else:
                image_data = capture_usbcam()
    except Exception as e:
        print("An error occurred while attempting to capture an image.")
        return {}

    resp = requests.post(f"http://{DESKTOP_IP}:5000/api/skin", data=image_data)
    return resp.json()
