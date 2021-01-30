import requests
import yaml

CONFIG_DIR = "config.yml"  # Use mycroft-core directory - updating file inside skill folder causes reload
DESKTOP_IP = None
CONFIG = None

try:
    with open("config.yml", "r") as config_data:
        CONFIG = yaml.load(config_data, Loader=yaml.BaseLoader)
        DESKTOP_IP = CONFIG["DESKTOP_IP"]
        print(f"Loaded DESKTOP_IP={DESKTOP_IP}")
except IOError:
    print("config.yml does not exist! Generating default config.yml...")
    d = {"DESKTOP_IP": "127.0.0.1:5000"}
    file = open("config.yml", "w")
    file.write(yaml.dump(d))
    exit()

DESK_SERVER_URL = f"http://{DESKTOP_IP}/api"


""" Testing flow:
1. Start everything up
2. Enqueue patients by calling the desk-server API endpoint
3. Tell AIMAR to go check up on the next patient
4. Observe what happens
"""


def register_patient(full_name, image_data):
    """ Patient ID is generated on the server side """
    try:
        resp = requests.post(f"{DESK_SERVER_URL}/patient/insert?full_name={full_name}", image_data)
    except requests.exceptions.ConnectionError:
        return False

    return resp


def query_patient(patient_id):
    """ Returns patient information and a room number if they are currently assigned to one. """
    try:
        resp = requests.get(f"{DESK_SERVER_URL}/patient/query?patient_id={str(patient_id)}")
    except requests.exceptions.ConnectionError:
        return False

    return resp.json()


def verify_patient(patient_id, image_data):
    """ Verify if patient_id matches with face image. Done when the robot arrives in the checkup room.
        patient_id should already be provided, while image_data is provided by aimar_camera.capture_image(). """

    try:
        resp = requests.post(f"{DESK_SERVER_URL}/patient/verify?patient_id={patient_id}", data=image_data)
    except requests.exceptions.ConnectionError:
        return None

    return resp


def match_patient(full_name, image_data):
    """ Get patient's ID using their name and face image.
    :return: None on error, -1 if full_name not in database, -2 if no faces match up.
    """
    try:
        resp = requests.post(f"{DESK_SERVER_URL}/patient/match?full_name={full_name}", data=image_data)
    except requests.exceptions.ConnectionError:
        return None

    return resp


def enqueue_patient(patient_id, room_number):
    """ Adds a patient id to the checkup queue. Patients are enqueued outside of Mycroft.
        e.g. run enqueue_patient(...) in a Python console."""
    try:
        resp = requests.post(f"{DESK_SERVER_URL}/patient/enqueue?patient_id={str(patient_id)}&room_number={str(room_number)}")
    except requests.exceptions.ConnectionError:
        return False

    return resp


def dequeue_patient():
    """ Gets a patient from the checkup queue and the coordinates to navigate to. """
    try:
        resp = requests.post(f"{DESK_SERVER_URL}/patient/dequeue")
    except requests.exceptions.ConnectionError:
        return False

    patient_id = int(resp.json()['patient_id'])
    return patient_id


def get_room_coords(room_number):
    try:
        resp = requests.get(f"{DESK_SERVER_URL}/room/coordinates?room_number={room_number}")
    except requests.exceptions.ConnectionError:
        return False

    x, y = float(resp.json()['x']), float(resp.json()['y'])
    return x, y


def diagnose_skin_image(image_data):
    try:
        resp = requests.post(f"http://{DESKTOP_IP}/api/skin", data=image_data)
        resp_json = resp.json()
        report_text = ""
        for key in resp_json:
            report_text += f"{key}: {100*float(resp_json[key]):.1f}%\n"
        return report_text
    except OSError:
        return None
