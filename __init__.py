from mycroft import MycroftSkill, intent_file_handler
from skills.aimar import aimar_arm

global swift
swift = None

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

def stop(self):
    pass

def create_skill():
    return Aimar()
