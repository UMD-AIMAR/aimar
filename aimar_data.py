import requests
from skills.mycroft_aimar import aimar_util

PATIENT_API_URL = f"http://{aimar_util.DESKTOP_IP}/api/patient"


# Patient ID is generated on the server side
def register_patient(full_name, image_data):
    try:
        resp = requests.post(f"{PATIENT_API_URL}/insert?full_name={full_name}", image_data)
    except requests.exceptions.ConnectionError:
        return False

    return resp


# Returns True/False on whether the ID is in the table.
def is_patient_registered(patient_id):
    try:
        resp = requests.post(f"{PATIENT_API_URL}/query?patient_id={str(patient_id)}")
    except requests.exceptions.ConnectionError:
        return False

    return resp


# Verify if patient_id matches with face image.
def verify_patient(patient_id, image_data):
    try:
        resp = requests.post(f"{PATIENT_API_URL}/verify?patient_id={patient_id}", data=image_data)
    except requests.exceptions.ConnectionError:
        return None

    return resp


# Identify patient through name and face image data.
def get_patient_id(full_name, image_data):
    """
    :return: None on error, -1 if full_name not in database, -2 if no faces match up.
    """
    try:
        resp = requests.post(f"{PATIENT_API_URL}/fetch?full_name={full_name}", data=image_data)
    except requests.exceptions.ConnectionError:
        return None

    return resp


# Adds a patient id to the checkup queue.
def enqueue_patient(patient_id):
    try:
        resp = requests.post(f"{PATIENT_API_URL}/enqueue?patient_id={str(patient_id)}")
    except requests.exceptions.ConnectionError:
        return False

    return resp
