import time

swift = None

try:
    from skills.mycroft_aimar.uarm.wrapper import SwiftAPI
    swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
    swift.waiting_ready()
except ImportError:
    print("Warning: SwiftAPI library not detected.")
except Exception:
    print("Warning: No uArm detected.")


def test():
    global swift
    if swift:
        # swift.get_gripper_catch()
        # swift.get_polar()
        swift.reset()
        time.sleep(3)
        swift.set_polar(stretch=120, rotation=70, height=-10, wait=True)

