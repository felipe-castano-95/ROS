#!/usr/bin/env python

import rospy
from random import uniform
from turtlesim.msg import Pose

# Genera una posición (X, Y) aleatoria y crea un objeto Pose para enviar
def get_location():
    pose = Pose()
    pose.x = round(uniform(0, 11.09), 2)
    pose.y = round(uniform(0, 11.09), 2)
    pose.theta = 0.0
    pose.linear_velocity = 0.0
    pose.angular_velocity = 0.0
    return pose

# Se inicia el Publisher y publica una posición periodicamente
def talker():
    pub = rospy.Publisher('turtlesim_go_to_talker', Pose, queue_size=10)
    rospy.init_node('turtlesim_go_to_talker', anonymous=True)
    n = 0.05
    rate = rospy.Rate(n) # 10hz
    while not rospy.is_shutdown():
        pose_message = get_location()
        rospy.loginfo(pose_message)
        pub.publish(pose_message)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
