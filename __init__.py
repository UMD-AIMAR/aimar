from mycroft import MycroftSkill, intent_file_handler
from skills.mycroft_aimar import aimar_arm, aimar_skin, aimar_move


class Aimar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('drive.intent')
    def handle_drive(self, message):
        time = message.data.get('time')
        direction = message.data.get('direction')

        aimar_move.move_simple(time, direction)

        if time is not None:
            self.speak_dialog('drive', {'time': time, 'direction': direction})
        else:
            self.speak_dialog('drive.generic')

    @intent_file_handler('uarm.test.intent')
    def handle_uarm_test(self, message):
        self.speak_dialog('uarm.test')
        aimar_arm.test()

    @intent_file_handler('skin.intent')
    def handle_skin_intent(self, message):
        resp_text = aimar_skin.capture_photo_and_diagnose()

        if resp_text is not None:
            self.speak_dialog('skin', {'resp_text': resp_text})
        else:
            self.speak_dialog('skin.generic')

    # Patient Interactions
    @intent_file_handler('patient.register.intent')
    def handle_patient_register_intent(self, message):
        self.set_context("name_tx")
        patient_name = self.get_response("Okay. What's your name?")
        if patient_name:
            patient_age = self.get_response("How old are you?")
            if patient_age:
                self.speak(f'{patient_name} is {patient_age} years old.')


def stop(self):
    pass


def create_skill():
    return Aimar()
