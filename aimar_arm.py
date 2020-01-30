from skills.mycroft_aimar.uarm.wrapper import SwiftAPI
from skills.mycroft_aimar.uarm.tools.list_ports import get_ports
import time

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready()

def test():
    # swift.get_gripper_catch()
    # swift.get_polar()
    swift.reset()
    time.sleep(3)
    swift.set_polar(stretch=120, rotation=70, height=-10, wait=True)
