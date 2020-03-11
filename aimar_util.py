import yaml

CONFIG = None
DESKTOP_IP = None


def init():
    global CONFIG, DESKTOP_IP
    try:
        with open("config.yml", "r") as config_data:
            CONFIG = yaml.load(config_data, Loader=yaml.BaseLoader)
            DESKTOP_IP = CONFIG["DESKTOP_IP"]
    except IOError:
        print("config.yml does not exist! Generating default config.yml...")
        d = {"DESKTOP_IP": "127.0.0.1"}
        file = open("config.yml", "w")
        file.write(yaml.dump(d))
        exit()
