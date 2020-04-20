import yaml
import os

AIMAR_SKILL_DIR = os.path.join(".", "skills", "mycroft_aimar")  # not used
CONFIG_DIR = "config.yml"  # Use mycroft-core directory - updating file inside skill folder causes reload
DESKTOP_IP = None
CONFIG = None

try:
    with open("config.yml", "r") as config_data:
        CONFIG = yaml.load(config_data, Loader=yaml.BaseLoader)
        DESKTOP_IP = CONFIG["DESKTOP_IP"]
        print(f"Loaded DESKTOP_IP={DESKTOP_IP}")
except IOError:
    print("config.yml does not exist! Generating default config.yml...")
    d = {"DESKTOP_IP": "127.0.0.1:5000"}
    file = open("config.yml", "w")
    file.write(yaml.dump(d))
    exit()


def checkup_loop():
    """ A repeating task where AIMAR checks up on patients. Patients should be specified by ID + a room.

    1. Navigate to the patient's location. We can either:
        a. Ask for a room number
        b. Already know which room where the patient is in (via some database)
        c. Tell the robot to 'follow me'
    2. Arrive at patient's room.
        a. Optionally verify the patient is in the room through facial recognition.
    3. Begin talking to the patient.
        a. Ask/identify the main category of illness the patient is here for.
           There should be an individual code module for each illness.
        b. General diagnosis questions: time/severity of symptoms, etc.
        c. Take measurements as needed. Depends on the module.
        d. Save all of this data to the central computer so the doctor can pull it up.
    4. Leave the room.
        a. check up on the next patient, if one is in the 'queue'
        b. If not, goes back to the 'control room'.
    """
    return False
