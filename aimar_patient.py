import requests
DESKTOP_URL = "10.0.0.5:5000"


# Maybe we will do this with a ROS node?
# Patient ID is generated on the server side
def register_patient(data):
    resp = requests.post(DESKTOP_URL + "/api/patient/insert", data)
    return resp
