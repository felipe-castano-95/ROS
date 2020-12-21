#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import pow,atan2,sqrt


pose = Pose()
tolerance = 1.5
velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

def get_distance(goal_x, goal_y):
    distance = sqrt(pow((goal_x - pose.x), 2) + pow((goal_y - pose.y), 2))
    return distance

def steering_angle(goal_x, goal_y):
	global pose
	return atan2(goal_y - pose.y, goal_x - pose.x) - pose.theta

def get_position(data):
	global pose
	pose = data
	pose.x = round(data.x, 2)
	pose.y = round(data.y, 2)
	#rospy.loginfo('I heard %s', data)

def create_twist_message(distance, angle):
	twist_msg = Twist()
	twist_msg.linear.x = distance 
	twist_msg.linear.y = 0
	twist_msg.linear.z = 0
  
  	# Angular velocity in the z-axis.
	twist_msg.angular.x = 0
	twist_msg.angular.y = 0
	twist_msg.angular.z = angle
	return twist_msg

def move(goal, rate):
	global pose

	rospy.loginfo("pose %s", pose)
	rospy.loginfo("goal %s", goal)

	angle = steering_angle(goal.x, goal.y)
	distance = get_distance(goal.x, goal.y)

	while(abs(angle) > 0.01):
		twist_msg = create_twist_message(0, angle)
		velocity_publisher.publish(twist_msg)
		rate.sleep()
		angle = steering_angle(goal.x, goal.y)
		rospy.loginfo("angle %s", angle)

	while(distance > tolerance):
		twist_msg = create_twist_message(distance, 0)
		velocity_publisher.publish(twist_msg)
		rate.sleep()

		#rospy.loginfo("distance %s", distance)
		distance = get_distance(goal.x, goal.y)
		rospy.loginfo("distance %s", distance)

		if(pose.x > 9 or pose.x < 1 or pose.y > 9 or pose.y < 1):
			break


	rospy.loginfo("Termine")


def callback(data, args):
	goal = data
	move(goal, args[0])

def listener():
    rospy.init_node('turtlesim_go_to_listener', anonymous=True)
    rate = rospy.Rate(0.5)
    rospy.Subscriber('turtlesim_go_to_talker', Pose, callback, (rate,))
    rospy.Subscriber('turtle1/pose', Pose, get_position)
    rospy.spin()

if __name__ == '__main__':
    listener()
