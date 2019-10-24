from mycroft import MycroftSkill, intent_file_handler


class Aimar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('left.intent')
    def handle_aimar(self, message):
        self.speak_dialog('left')

def stop(self):
    pass

def create_skill():
    return Aimar()

