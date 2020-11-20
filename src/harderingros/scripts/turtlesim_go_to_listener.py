#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

def get_position(data):
    rospy.loginfo(data)

def calculate_next_step():
    pass

def callback(data):
    steps = 10
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)

def listener():
    rospy.init_node('turtlesim_go_to_listener', anonymous=True)
    rospy.Subscriber('turtlesim_go_to_talker', Pose, callback)
    rospy.Subscriber('turtle/pose', Pose, get_position)
    rospy.spin()

if __name__ == '__main__':
    listener()
