import requests
from skills.mycroft_aimar import aimar_util

PATIENT_API_URL = f"http://{aimar_util.DESKTOP_IP}/api/patient"


""" Testing flow:
1. Start everything up
2. Enqueue patients by calling the desk-server API endpoint
3. Tell AIMAR to go check up on the next patient
4. Observe what happens
"""


def register_patient(full_name, image_data):
    """ Patient ID is generated on the server side """
    try:
        resp = requests.post(f"{PATIENT_API_URL}/insert?full_name={full_name}", image_data)
    except requests.exceptions.ConnectionError:
        return False

    return resp


def is_patient_registered(patient_id):
    """ Returns True/False on whether the ID is in the table. """
    try:
        resp = requests.post(f"{PATIENT_API_URL}/query?patient_id={str(patient_id)}")
    except requests.exceptions.ConnectionError:
        return False

    return resp


def verify_patient(patient_id, image_data):
    """ Verify if patient_id matches with face image. Done when the robot arrives in the checkup room.
        patient_id should already be provided, while image_data is provided by aimar_camera.capture_image(). """

    try:
        resp = requests.post(f"{PATIENT_API_URL}/verify?patient_id={patient_id}", data=image_data)
    except requests.exceptions.ConnectionError:
        return None

    return resp


def get_patient_id(full_name, image_data):
    """ Get patient's ID using their name and face image.
    :return: None on error, -1 if full_name not in database, -2 if no faces match up.
    """
    try:
        resp = requests.post(f"{PATIENT_API_URL}/fetch?full_name={full_name}", data=image_data)
    except requests.exceptions.ConnectionError:
        return None

    return resp


# PATIENT_API_URL = "http://10.0.0.10:5000/api/patient"
def enqueue_patient(patient_id, room_number):
    """ Adds a patient id to the checkup queue. """
    try:
        resp = requests.post(f"{PATIENT_API_URL}/enqueue?patient_id={str(patient_id)}&room_number={str(room_number)}")
    except requests.exceptions.ConnectionError:
        return False

    return resp


def dequeue_patient():
    """ Gets a patient from the checkup queue and the coordinates to navigate to. """
    try:
        resp = requests.post(f"{PATIENT_API_URL}/dequeue")
    except requests.exceptions.ConnectionError:
        return False

    patient_id = int(resp.json()['patient_id'])
    room_coordinates = resp.json()['coordinates']
    return patient_id, room_coordinates

