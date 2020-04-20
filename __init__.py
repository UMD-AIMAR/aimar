from mycroft import MycroftSkill, intent_file_handler
from skills.mycroft_aimar import aimar_data, aimar_camera, aimar_arm, aimar_move, aimar_util


class Aimar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('drive.intent')
    def handle_drive(self, message):
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

    @intent_file_handler('uarm.test.intent')
    def handle_uarm_test(self, message):
        self.speak("I'm moving my arm.")
        aimar_arm.test()

    @intent_file_handler('skin.intent')
    def handle_skin_intent(self, message):
        image_data = aimar_camera.capture_image()
        if image_data is None:
            self.speak("Sorry, I don't detect any cameras plugged in.")
            return

        report_text = aimar_camera.diagnose_skin_image(image_data)
        image_path = f"/home/kevin/mycroft-core/{aimar_camera.TEMP_IMAGE_PATH}"
        if report_text is None:
            response = "Sorry, I couldn't analyze your skin image."
        else:
            response = "I've analyzed your image and displayed the results."

        self.speak(response)
        self.gui.show_image(image_path, title=report_text, caption=response, fill="PreserveAspectFit", override_idle=10)

    # TODO: get a live video feed on the mycroft gui, show a picture timer. maybe neither is possible
    @intent_file_handler('patient.register.intent')
    def handle_patient_register_intent(self, message):
        """ Asks the patient for their name and a picture. Stores this info as an entry in the database. """
        q_name = "What's your name?"
        self.gui.show_text(q_name)
        full_name = self.get_response(q_name)
        if full_name is None:
            self.speak("Okay, we'll register you some other time,")
            return

        image_data = aimar_camera.capture_image()
        if image_data is None:
            self.speak("I can't register you at this time, since I don't have any cameras plugged in.")
            return

        registered_status = aimar_data.register_patient(full_name, image_data)
        if registered_status:
            self.speak(f"Ok {full_name}, you're now registered!")
        else:
            self.speak(f"Sorry {full_name}, I can't register you at this time.")

    @intent_file_handler('patient.enqueue.intent')
    def handle_patient_enqueue_intent(self, message):
        """ Fetches a patient's id with their full name + face image, then puts them in the checkup queue.
            This may be done by a robot in the lobby, while other AIMAR units do the actual checkups.
            We can also manually enqueue patients by adding database entries server-side.
        """
        full_name = message.data.get('full_name')
        image_data = aimar_camera.capture_image()
        if image_data is None:
            self.speak("I can't sign you in at this time, since I don't have any cameras plugged in.")
            return

        patient_id = aimar_data.get_patient_id(full_name, image_data)
        if patient_id is None:
            response_dialog = f"Sorry, I encountered an error while trying to identify you."
        elif patient_id == -1:
            response_dialog = f"{full_name} was not found in the patient database. Please register first."
        elif patient_id == -2:
            response_dialog = f"Your face does not match up with any patient named {full_name}."
        else:
            response_dialog = f"Okay {full_name}, we will be with you shortly."
            aimar_data.enqueue_patient(patient_id)

        image_path = f"/home/kevin/mycroft-core/{aimar_camera.TEMP_IMAGE_PATH}"
        self.speak(response_dialog)
        self.gui.show_image(image_path, fill="PreserveAspectFit", override_idle=10)

    @intent_file_handler('patient.verify.intent')
    def handle_patient_verify_intent(self, message):
        patient_id = message.data.get('patient_id')
        image_data = aimar_camera.capture_image()
        if image_data is None:
            self.speak("I can't sign you in at this time, since I don't have any cameras plugged in.")
            return

        is_match = aimar_data.verify_patient(patient_id, image_data)
        if is_match:
            response_dialog = "Matched"
        else:
            response_dialog = "Not matched"

        image_path = f"/home/kevin/mycroft-core/{aimar_camera.TEMP_IMAGE_PATH}"
        self.speak(response_dialog)
        self.gui.show_image(image_path, fill="PreserveAspectFit", override_idle=10)

    @intent_file_handler('cancel.intent')
    def handle_cancel_intent(self, message):
        self.gui.clear()


def stop(self):
    pass


def create_skill():
    return Aimar()
