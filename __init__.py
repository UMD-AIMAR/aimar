from mycroft import MycroftSkill, intent_file_handler
from skills.mycroft_aimar import aimar_data, aimar_camera, aimar_arm, aimar_move, aimar_util


class Aimar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    # Patients are enqueued outside of Mycroft.
    # e.g. run enqueue_patient(...) in a Python console.
    @intent_file_handler('patient.checkup.intent')
    def handle_patient_checkup_intent(self, message):
        """ Check up the next patient, then return to the starting room. """
        # aimar_util.checkup_next_patient()
        patient_id = aimar_data.dequeue_patient()
        patient_data = aimar_data.query_patient(patient_id)
        room_number = patient_data['room_number']
        patient_name = patient_data['patient_info'][1]

        response = self.ask_yesno(f"The next patient is {patient_name}, in room {room_number}. Should I check on them?")
        if response == 'yes':
            x, y = aimar_data.get_room_coords(room_number)
            self.speak(f"Okay, I'm going to {room_number}, which is at coordinates {x}, {y}")
            aimar_move.send_goal(x, y)
        else:
            self.speak("Okay, I'll keep waiting.")

    """
    Other intents are defined here for individual component testing.
    """

    # In terminal:
    # Gazebo:     ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
    # Navigation: ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/map.yaml
    #
    # Mycroft:    ./start-mycroft.sh cli
    @intent_file_handler('move.goal.intent')
    def handle_move_goal(self, message):
        room_number = message.data.get('room_number')
        if room_number is not None:
            x, y = aimar_data.get_room_coords(room_number)
        else:
            x = float(message.data.get('x'))
            y = float(message.data.get('y'))

        if x is not None and y is not None:
            aimar_move.send_goal(x, y)
            self.speak_dialog(f"Moving to coordinates {x}, {y}")
        else:
            self.speak_dialog(f"I couldn't understand your command.")

    @intent_file_handler('move.simple.intent')
    def handle_move_simple(self, message):
        time = message.data.get('time')
        direction = message.data.get('direction')
        if time and direction:
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
