import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class MovementPublisher(Node):

    def __init__(self):
        super().__init__('movement_publisher')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

    def publish(self, msg):
        self.publisher_.publish(msg)


def move_simple(time, direction):
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


def move_stop():
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    vel_pub.publish(vel_msg)


rclpy.init()
vel_pub = MovementPublisher()
# movement_publisher.destroy_node()
# rclpy.shutdown()
