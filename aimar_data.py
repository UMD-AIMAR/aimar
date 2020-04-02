import requests
from skills.mycroft_aimar import aimar_util


# Maybe we will do this with a ROS node?
# Patient ID is generated on the server side
def register_patient(data):
    try:
        resp = requests.post(f"http://{aimar_util.DESKTOP_IP}/api/patient/insert", data)
    except requests.exceptions.ConnectionError:
        return False

    return resp
