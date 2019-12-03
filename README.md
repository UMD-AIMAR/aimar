# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg" card_color="#40DBB0" width="50" height="50" style="vertical-align:bottom"/> Aimar
Controls the aimar robot.

## About
Controls the aimar robot with commands for movement, navigation, image recognition, and more.

The AIMAR skill runs alongside Mycroft. Mycroft uses Python 3 and runs on the TurtleBot.

The skill executes arm movements using the uArm-Python-SDK. \_\_init\_\_.py (skill file) should not directly call SDK functions.
Instead, \_\_init\_\_.py imports aimar_arm.py and the SDK is imported in aimar_arm.py.

To send ROS messages (if we are using a library that uses ROS subscribers), we have to write ROS publishser/subscriber code.
This has to be written in the robot-server application, since ROS Kinetic uses Python 2.
We can then make a call to robot-server by using a web request.

For functions like database access and skin image classification, we send a web request to desk-server.

## Setup
Download uArm-Python-SDK: https://github.com/uArm-Developer/uArm-Python-SDK

Copy 'uArm-Python-SDK/uarm' folder into 'aimar' folder

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

