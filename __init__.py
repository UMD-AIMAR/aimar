from mycroft import MycroftSkill, intent_file_handler
from skills.mycroft_aimar import aimar_arm, aimar_skin, aimar_move, aimar_patient


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
        resp_text = aimar_skin.diagnose_image(aimar_skin.capture_picam())

        if resp_text is not None:
            self.speak_dialog('skin', {'resp_text': resp_text})
        else:
            self.speak_dialog('skin.generic')

    # Patient Interactions
    @intent_file_handler('patient.register.intent')
    def handle_patient_register_intent(self, message):
        responses = {
            # 'patient_id': "INTEGER PRIMARY KEY",
            'first_name': "What's your first name?",
            'last_name': "What about your last name?",
            'gender': "What's your gender?",
            'age': "How old are you?",
            'state': "What state do you live in?",
            'street_address': "What's your street address?",
            'zip_code': "What's your zip code?",
            'phone_number': "What's your phone number?"
        }
        order = ['first_name', 'last_name', 'age', 'gender', 'state', 'street_address', 'zip_code', 'phone_number']
        patient_data = {}
        for key in order:
            patient_data[key] = self.get_response(responses[key])
        aimar_patient.register_patient(patient_data)
        self.speak("You are registered now!")


def stop(self):
    pass


def create_skill():
    return Aimar()
