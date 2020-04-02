import yaml
import os

AIMAR_SKILL_DIR = os.path.join(".", "skills", "mycroft_aimar")  # not used
CONFIG_DIR = "config.yml"  # Use mycroft-core directory - updating file inside skill folder causes reload
DESKTOP_IP = None
CONFIG = None


def init():
    global CONFIG, DESKTOP_IP
    try:
        with open("config.yml", "r") as config_data:
            CONFIG = yaml.load(config_data, Loader=yaml.BaseLoader)
            DESKTOP_IP = CONFIG["DESKTOP_IP"]
    except IOError:
        print("config.yml does not exist! Generating default config.yml...")
        d = {"DESKTOP_IP": "127.0.0.1:5000"}
        file = open("config.yml", "w")
        file.write(yaml.dump(d))
        exit()
