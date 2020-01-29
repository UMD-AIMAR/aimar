# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg" card_color="#40DBB0" width="50" height="50" style="vertical-align:bottom"/> Aimar
[UMD-AIMAR](https://github.com/UMD-AIMAR)

This repository is a Mycroft "Skill". It handles all of the user speech and figuring out what action they want AIMAR to perform.

![AIMAR Diagram](https://raw.githubusercontent.com/UMD-AIMAR/mycroft-aimar/master/AIMAR-pieces.png)
## About

uArm code goes in [aimar_arm.py](https://github.com/UMD-AIMAR/mycroft-aimar/blob/master/aimar_arm.py). Note that [\_\_init.py\_\_](https://github.com/UMD-AIMAR/mycroft-aimar/blob/master/__init__.py) imports aimar_arm.

ROS messaging code goes in [robot-server](https://github.com/UMD-AIMAR/robot-server), since ROS Kinetic uses Python 2. We can then make a call to robot-server by using a web request to localhost.

Database and Skin Image Classification goes in [desk-server](https://github.com/UMD-AIMAR/desk-server). Voice commands can trigger these functions by making a web request to the desktop: https://github.com/UMD-AIMAR/mycroft-aimar/blob/master/__init__.py#L44.

## Setup
Windows: Download [Git](https://gitforwindows.org/), then open Git Bash.

Mac: Open a terminal.

Run `git clone https://github.com/UMD-AIMAR/mycroft_aimar.git`

Download [uArm-Python-SDK](https://github.com/uArm-Developer/uArm-Python-SDK): `git clone https://github.com/uArm-Developer/uArm-Python-SDK.git`

Copy 'uArm-Python-SDK/uarm' folder into 'mycroft-aimar' folder

## Examples
* "Turn left"
* "Drive to the conference room"
* "Identify this skin condition"

## Credits
Team AIMAR

## Category
**IoT**
Transport

## Tags
#Robot
#Medical

