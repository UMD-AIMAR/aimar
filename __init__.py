from mycroft import MycroftSkill, intent_file_handler


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

def stop(self):
    pass

def create_skill():
    return Aimar()

