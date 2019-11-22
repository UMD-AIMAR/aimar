from mycroft import MycroftSkill, intent_file_handler
import aimar_arm

class Aimar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('left.intent')
    def handle_left(self, message):
        self.speak_dialog('left')

    @intent_file_handler('drive.forward.intent')
    def handle_drive_forward(self, message):
        time = message.data.get('time')
        if time is not None:
            self.speak_dialog('drive.forward', {'time': time})
        else:
            self.speak_dialog('drive.forward.generic')

# executing movement: send request to localhost:5000/api/bot/move?direction=???

    @intent_file_handler('uarm.test.intent')
    def handle_uarm_test(self, message):
        aimar_arm.test()

def stop(self):
    pass

def create_skill():
    return Aimar()

