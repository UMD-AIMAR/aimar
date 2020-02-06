import requests
DESKTOP_URL = "10.0.0.5:5000"


def register_patient(data):
    resp = requests.post(DESKTOP_URL + "/api/patient/insert", data)
    return resp
