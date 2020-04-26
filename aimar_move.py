import time
import rclpy
from rclpy.node import Node

# For simple movement
from geometry_msgs.msg import Twist

# For goal_pose
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from builtin_interfaces.msg import Time


class MovementPublisher(Node):

    def __init__(self):
        super().__init__('movement_publisher')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

    def publish(self, msg):
        self.publisher_.publish(msg)


class GoalPublisher(Node):

    def __init__(self):
        super().__init__('goal_publisher')
        self.publisher_ = self.create_publisher(PoseStamped, '/move_base_simple/goal', 10)

    def publish(self, msg):
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)


rclpy.init()
vel_pub = MovementPublisher()
goal_pub = GoalPublisher()


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
    while elapsed < time_limit:
        elapsed = time.time() - start

    move_stop()


"""
create_goal_pose: utility function to create the ROS message with target position information
send_goal: creates a ROS 'PoseStamped' message and tells the robot to move to that position.
"""


def create_goal_pose(x, y):
    pose = PoseStamped(
        header=Header(
            stamp=Time(sec=0, nanosec=0),
            frame_id='map'),
        pose=Pose(
            position=Point(x=x, y=y, z=0.0),
            orientation=Quaternion(x=0.0, y=0.0, z=0.0, w=1.0))
    )
    return pose


def send_goal(x, y):
    msg = create_goal_pose(x, y)
    goal_pub.publish(msg)

# node.destroy_node()
# rclpy.shutdown()
