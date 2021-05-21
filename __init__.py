import os
import time

from mycroft import MycroftSkill, intent_file_handler, AdaptIntent, intent_handler
import traceback
import sys

AIMAR_DIR = "/home/kevin/mycroft-core/skills/mycroft_aimar"
if AIMAR_DIR not in sys.path:
    sys.path.append(AIMAR_DIR)

try:
    from modules import symptomchecker
except ImportError as e:
    print()
    traceback.print_exc()
    print()
try:
    import aimar_util
except ImportError as e:
    print()
    traceback.print_exc()
    print()
try:
    import aimar_camera
except ImportError as e:
    print()
    traceback.print_exc()
    print()
try:
    import aimar_arm
except ImportError as e:
    print()
    traceback.print_exc()
    print()
try:
    import aimar_move
except ImportError as e:
    print()
    traceback.print_exc()
    print()


class AIMAR(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('patient.checkup.intent')
    def handle_patient_checkup_intent(self, message):
        """ Move to the next queued room. """
        patient_data = aimar_util.dequeue_patient()
        room_number = patient_data['room']
        patient_id = patient_data['id']

        self.aimar_show_image(f"I'm going to see patient ID {patient_id}, in room {room_number}", "aimar.png", 126, speak=True)
        x, y = aimar_util.get_room_coords(room_number)
        aimar_move.send_goal(x, y)

    # Medical chatbot
    @intent_file_handler('medicalchatbot.intent')
    def handle_category_diagnosis(self, message):
        response = self.get_response("Tell me about your problem.", on_fail=" ", )
        symptom, questions = symptomchecker.match(response)
        while not response or not symptom:
            response = self.get_response("I don't know that symptom.", on_fail=" ", )
            symptom, questions = symptomchecker.match(response)

        responses = []
        for i, (question_prefix, choices) in enumerate(questions):
            choices = [f.lower() for f in choices]
            # Create next question
            max_i = min(2, len(choices) - 1)
            question = f"{question_prefix} {', '.join(choices[:max_i])}"
            if len(choices) == 1:
                question += f"{choices[max_i]}?"
            else:
                question += f", or {choices[max_i]}?"
            if (i == 0):
                question += " You may also describe similar symptoms which are not on the list of options, and I'll try my best to understand."
            self.gui.show_text(question)
            response = self.get_response(question, on_fail=" ")
            responses.append(response)

        self.speak("Thank you. I am now logging our conversation.")
        symptomchecker.save_dialog(questions, responses)

    def aimar_show_video(self, header_text, video_path):
        self.gui.clear()
        self.gui['videoSource'] = video_path
        self.gui['headerText'] = header_text
        self.gui.show_page("video.qml")

    def aimar_show_image(self, header_text, image_path, height=270, refresh=True, speak=None):
        if refresh:
            self.gui.clear()
        self.gui['imageSource'] = image_path
        self.gui['headerText'] = header_text
        self.gui['imageHeight'] = height
        self.gui.show_page("image.qml")
        if speak:
            if speak == 'ask':
                response = self.get_response(header_text)
                return response
            else:
                self.speak(header_text)
    
    # In terminal:
    # Gazebo:     ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
    # Navigation: ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/map.yaml
    #
    # Mycroft:    ./start-mycroft.sh cli
    @intent_file_handler('move.goal.intent')
    def handle_move_goal(self, message):
        room_number = message.data.get('room_number')
        if room_number is not None:
            x, y = aimar_util.get_room_coords(room_number)
        else:
            x = float(message.data.get('x'))
            y = float(message.data.get('y'))

        if x is not None and y is not None:
            aimar_move.send_goal(x, y)
            self.speak_dialog(f"Moving to coordinates {int(x)}, {int(y)}")
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
        image_data, image_path = aimar_camera.capture_image()
        if image_data is None:
            self.speak("Sorry, I don't detect any cameras plugged in.")
            return

        report_text = aimar_util.diagnose_skin_image(image_data)
        if report_text is None:
            response = "Sorry, I couldn't analyze your skin image."
        else:
            response = "I've analyzed your image and displayed the results."

        self.speak(response)
        self.aimar_show_image("Skin image:", image_path, 126)

    # TODO: get a live video feed on the mycroft gui, show a timer for how long pictures last. maybe neither is possible
    @intent_file_handler('patient.register.intent')
    def handle_patient_register_intent(self, message):
        """ Asks the patient for their name and a picture. Stores this info as an entry in the database. """
        q_name = "What's your name?"
        self.aimar_show_image("What's your name?", "aimar.png", 126)
        full_name = self.get_response(q_name)
        if full_name is None:
            self.speak("Okay, we'll register you some other time,")
            return

        image_data, image_path = aimar_camera.capture_image()
        if image_data is None:
            self.speak("I can't register you at this time, since I don't have any cameras plugged in.")
            return

        registered_status = aimar_util.register_patient(full_name, image_data)
        if registered_status:
            self.speak(f"Ok {full_name}, you're now registered!")
        else:
            self.speak(f"Sorry {full_name}, I can't register you at this time.")

    @intent_file_handler('patient.verify.intent')
    def handle_patient_verify_intent(self, message):
        patient_id = message.data.get('patient_id')
        image_data, image_path = aimar_camera.capture_image()
        if image_data is None:
            self.speak("I can't sign you in at this time, since I don't have any cameras plugged in.")
            return

        is_match = aimar_util.verify_patient(patient_id, image_data)
        if is_match:
            response_dialog = "Matched"
        else:
            response_dialog = "Not matched"

        self.speak(response_dialog)
        self.gui.show_image(image_path, fill="PreserveAspectFit", override_idle=10)

    @intent_file_handler('cancel.intent')
    def handle_cancel_intent(self, message):
        self.gui.clear()


def stop(self):
    pass


def create_skill():
    return AIMAR()
