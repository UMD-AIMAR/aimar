import time

from skills.aimar.uarm.wrapper import SwiftAPI
from skills.aimar.uarm.tools.list_ports import get_ports

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready()

def test():
    global swift
    speed = 50
    swift.get_gripper_catch()
    swift.get_polar()
    while swift.connected:

        swift.set_polar(stretch=200, rotation=80, height=150, wait=True)
        swift.set_polar(stretch=200, rotation=80, height=0, wait=True)
        swift.set_gripper(catch=True, wait =True)
        time.sleep(3)
        swift.set_polar(stretch=150, rotation=80, height=150, wait = True)
        swift.set_polar(stretch=200, rotation=141, height=170, wait = True)
        swift.set_polar(stretch=200, rotation=141, height=142, wait = True)
        swift.set_gripper(catch=False, wait = False)
        time.sleep(3)