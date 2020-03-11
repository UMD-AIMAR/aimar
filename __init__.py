from mycroft import MycroftSkill, intent_file_handler
from skills.mycroft_aimar import aimar_util

aimar_util.init()

#
# Import each file. If import fails disable that individual set of functions.
arm_enabled, skin_enabled, move_enabled = False, False, False

print("Loading AIMAR Modules...")
print("----------------------------")

try:
    from skills.mycroft_aimar import aimar_arm
    arm_enabled = True
except ImportError as ex:
    print("ImportError (aimar_arm):", ex)
except Exception as ex:
    print(ex)

try:
    from skills.mycroft_aimar import aimar_skin
    skin_enabled = True
except ImportError as ex:
    print("ImportError (aimar_skin):", ex)

try:
    from skills.mycroft_aimar import aimar_move
    move_enabled = True
except ImportError as ex:
    print("ImportError (aimar_move):", ex)

try:
    from skills.mycroft_aimar import aimar_patient
    patient_enabled = True
except ImportError as ex:
    print("ImportError (aimar_patient):", ex)

print("Done loading!")

#
# Define constants
REGISTER_QUESTIONS = {
            'first_name': "What's your first name?",
            'last_name': "What about your last name?",
            'age': "How old are you?",
            'gender': "What's your gender?",
            'state': "What state do you live in?",
            'street_address': "What's your street address?",
            'zip_code': "What's your zip code?",
            'phone_number': "What's your phone number?"
        }
REGISTER_ORDER = ['first_name', 'last_name', 'age']  # 'gender', 'state', 'street_address', 'zip_code', 'phone_number'


#
# Intent handling
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
        image_data = aimar_skin.capture_image()
        if image_data == {}:
            self.speak("Sorry, I don't detect any cameras plugged in.")
            return

        self.gui.show_image("temp_skin.png")
        resp_text = aimar_skin.diagnose_image(image_data)

        if resp_text is None:
            self.speak("Sorry, I couldn't analyze your skin image.")
        else:
            self.speak_dialog('skin', {'resp_text': resp_text})

    @intent_file_handler('patient.register.intent')
    def handle_patient_register_intent(self, message):
        patient_data = {}
        for key in REGISTER_ORDER:
            self.gui.show_text(REGISTER_QUESTIONS[key])
            utterance = self.get_response(REGISTER_QUESTIONS[key])
            if utterance is not None:
                patient_data[key] = utterance
            else:
                self.speak("Okay, we'll register you some other time,")
                return

        registered_status = aimar_patient.register_patient(patient_data)
        if registered_status:
            self.speak(f"Ok {patient_data['first_name']}, you're now registered!")
        else:
            self.speak(f"Sorry {patient_data['first_name']}, I can't contact the patient database. "
                       f"We'll register you some other time.")


def stop(self):
    pass


def create_skill():
    return Aimar()
