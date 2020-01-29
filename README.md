# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg" card_color="#40DBB0" width="50" height="50" style="vertical-align:bottom"/> Aimar
[UMD-AIMAR](https://github.com/UMD-AIMAR)

This repository is a Mycroft "Skill". It handles all of the user speech and figuring out what action they want AIMAR to perform.

![AIMAR Diagram](https://raw.githubusercontent.com/UMD-AIMAR/mycroft-aimar/master/AIMAR-pieces.png)

What are [robot-server](https://github.com/UMD-AIMAR/robot-server) and [desk-server](https://github.com/UMD-AIMAR/desk-server)?

desk-server controls central systems like skin image processing and the patient database, and should run on a desktop. robot-server controls Turtlebot/arm movement, and should be downloaded to individual Turtlebots. These two applications allow us to link voice control, code running on the robot, and code on the desktop all together.

What **is** a server?

A server is an application that listens for incoming requests to a specific `address:port` value (e.g. `10.0.0.8:5000`). When it hears a request, it executes a function of code, which usually responds to the sender with some data (like a webpage). You can test this out yourself by opening cmd (for Mac, Terminal) and typing `curl https://google.com`. 

Suppose we have desk-server running on a desktop at address `10.0.0.8:5000`. When image data is sent to `10.0.0.8:5000/skin`, the server classifies the image and sends the diagnosis back as a response. Now we put Python code on the bot that takes an image, and sends the web request, and reads the web response out loud.

Example entire workflow:

1. "AIMAR, is there a problem with my skin?"

2. Mycroft hears this and runs mycroft_aimar/skin_command.py. (I'll make this soon)

3. skin_command.py captures a photo, then sends it in a web request to desk_server's address.

4. desk_server feeds the image to desk-server/skin.py and gets a prediction.

5. desk_server sends the diagnosis in a web response to skin_command.py.

6. Mycroft responds with the diagnosis.

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

