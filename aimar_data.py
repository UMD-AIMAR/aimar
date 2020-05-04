import requests
from skills.mycroft_aimar import aimar_util

DESK_SERVER_URL = f"http://{aimar_util.DESKTOP_IP}/api"


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
    """ Adds a patient id to the checkup queue. """
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
