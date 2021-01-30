import time
import rospy

from geometry_msgs.msg import Twist, PoseStamped, Pose, Point, Quaternion
from std_msgs.msg import Header

print("Initializing ROS node. Make sure roscore is running.")
rospy.init_node('aimar', disable_signals=True, anonymous=True)
time.sleep(1)
import os
print(os.system("rosnode list"))
vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)


"""
move_stop: Used by move_simple to stop the robot after a time delay. 
move_simple: Sends a commend for the turtlebot to move in a certain direction for X seconds.
"""


def move_stop():
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    vel_pub.publish(vel_msg)


def move_simple(time_limit, direction):
    speed = 2.0
    vel_msg = Twist()

    if direction == 'forward':
        vel_msg.linear.x = speed
    elif direction == 'backward':
        vel_msg.linear.x = -speed
    elif direction == 'right':
        vel_msg.angular.z = -speed
    elif direction == 'left':
        vel_msg.angular.z = speed
    else:
        return False
    vel_pub.publish(vel_msg)

    start = time.time()
    elapsed = 0
    while elapsed < int(time_limit):
        elapsed = time.time() - start

    move_stop()


"""
create_goal_pose: utility function to create the ROS message with target position information
send_goal: creates a ROS 'PoseStamped' message and tells the robot to move to that position.
"""


def create_goal_pose(x, y):
    pose = PoseStamped(
        header=Header(
            stamp=rospy.Time.now(),
            frame_id='map'),
        pose=Pose(
            position=Point(x=x, y=y, z=0.0),
            orientation=Quaternion(x=0.0, y=0.0, z=0.0, w=1.0))
    )
    return pose


def send_goal(x, y):
    msg = create_goal_pose(x, y)
    goal_pub.publish(msg)
