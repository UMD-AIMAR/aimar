import os

from mycroft import MycroftSkill, intent_file_handler
from skills.mycroft_aimar import aimar_util

"""
0. Desktop IP address is loaded in from config.yml.
"""
aimar_util.init()

"""
1. Import each file. If import fails disable that individual set of functions.
"""
uarm_enabled, skin_enabled, move_enabled, data_enabled = False, False, False, False

print("Loading AIMAR Modules...")
print("----------------------------")

try:
    from skills.mycroft_aimar import aimar_arm

    uarm_enabled = True
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
    from skills.mycroft_aimar import aimar_data

    data_enabled = True
except ImportError as ex:
    print("ImportError (aimar_patient):", ex)

print("Done loading!")

"""
2. Define some dialogs and file paths.
"""
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

UARM_DISABLED_DIALOG = "Sorry, my arm functions are currently disabled."
MOVE_DISABLED_DIALOG = "Sorry, my movement functions are currently disabled."
SKIN_DISABLED_DIALOG = "Sorry, my skin image analysis functions are currently disabled."
DATA_DISABLED_DIALOG = "Sorry, my patient data functions are currently disabled."


"""
3. Intent Handling
"""


class Aimar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('drive.intent')
    def handle_drive(self, message):
        if move_enabled:
            time = message.data.get('time')
            direction = message.data.get('direction')
            aimar_move.move_simple(time, direction)

            action = "moving"
            if direction == "left" or direction == "right":
                action = "turning"
            if time is None:
                self.speak_dialog(f"{action} {direction}")
            else:
                self.speak_dialog(f"{action} {direction} for {time} seconds")
        else:
            self.speak(MOVE_DISABLED_DIALOG)

    @intent_file_handler('uarm.test.intent')
    def handle_uarm_test(self, message):
        if uarm_enabled:
            self.speak("I'm moving my arm.")
            aimar_arm.test()
        else:
            self.speak(UARM_DISABLED_DIALOG)

    @intent_file_handler('skin.intent')
    def handle_skin_intent(self, message):
        if skin_enabled:
            image_data = aimar_skin.capture_image()
            if image_data is None:
                self.speak("Sorry, I don't detect any cameras plugged in.")
                return

            resp_text = aimar_skin.diagnose_image(image_data)
            image_path = f"/home/kevin/mycroft-core/{aimar_skin.TEMP_SKIN_IMAGE_PATH}"
            if resp_text is None:
                response_dialog = "Sorry, I couldn't analyze your skin image."
            else:
                response_dialog = "I've analyzed your image and displayed the results."

            self.speak(response_dialog)
            self.gui.show_image(image_path, title=resp_text,
                                caption=response_dialog, fill="PreserveAspectFit", override_idle=10)
        else:
            self.speak(SKIN_DISABLED_DIALOG)

    @intent_file_handler('patient.register.intent')
    def handle_patient_register_intent(self, message):
        if data_enabled:
            patient_data = {}
            for key in REGISTER_ORDER:
                self.gui.show_text(REGISTER_QUESTIONS[key])
                utterance = self.get_response(REGISTER_QUESTIONS[key])
                if utterance is not None:
                    patient_data[key] = utterance
                else:
                    self.speak("Okay, we'll register you some other time,")
                    return

            registered_status = aimar_data.register_patient(patient_data)
            if registered_status:
                self.speak(f"Ok {patient_data['first_name']}, you're now registered!")
            else:
                self.speak(f"Sorry {patient_data['first_name']}, I can't contact the patient database. "
                           f"We'll register you some other time.")
        else:
            self.speak(DATA_DISABLED_DIALOG)

    @intent_file_handler('cancel.intent')
    def handle_cancel_intent(self, message):
        self.gui.clear()


def stop(self):
    pass


def create_skill():
    return Aimar()
