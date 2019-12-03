import requests
import cv2
import io
import matplotlib.pyplot as plt

from mycroft import MycroftSkill, intent_file_handler
from skills.aimar import aimar_arm

DESKTOP_URL = "10.0.1.5"


class Aimar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('drive.intent')
    def handle_drive(self, message):
        time = message.data.get('time')
        direction = message.data.get('direction')
        # executing movement: send request to localhost:5000/api/bot/move?direction=???
        # after async delay stop
        if time is not None:
            self.speak_dialog('drive', {'time': time, 'direction': direction})
        else:
            self.speak_dialog('drive.generic')

    @intent_file_handler('uarm.test.intent')
    def handle_uarm_test(self, message):
        aimar_arm.test()

    @intent_file_handler('skin.intent')
    def handle_skin_intent(self, message):
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


def stop(self):
    pass


def create_skill():
    return Aimar()
