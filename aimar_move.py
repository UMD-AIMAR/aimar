import requests

ROBOT_URL = "localhost:5000"


def move_simple(time, direction):
    requests.get(f"{ROBOT_URL}/move?direction={direction}")
    # after async delay stop
