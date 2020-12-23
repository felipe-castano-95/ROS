#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import pow,atan2,sqrt


pose = Pose() # Objeto que tendra la posición de la tortuga en tiempo real
tolerance = 1.5 # Desviación minimo para llegar a la meta
velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

# Calcula la distancia entre la posición de la tortuga y la meta
def get_distance(goal_x, goal_y):
	global pose
    distance = sqrt(pow((goal_x - pose.x), 2) + pow((goal_y - pose.y), 2))
    return distance

# Calcula el angulo entre la posición de la tortuga y la meta teniendo en cuenta la posición a la que mira
def steering_angle(goal_x, goal_y):
	global pose
	return atan2(goal_y - pose.y, goal_x - pose.x) - pose.theta

# Obtiene y actualiza la posición de la tortuga en tiempo real
def get_position(data):
	global pose
	pose = data
	pose.x = round(data.x, 2)
	pose.y = round(data.y, 2)

# Crea un mensaje Twist recibiendo los pasos hacia el frente de la tortuga y el angulo en los que se movera
def create_twist_message(step, angle):
	twist_msg = Twist()
	twist_msg.linear.x = step 
	twist_msg.linear.y = 0
	twist_msg.linear.z = 0
  
  	# Angular velocity in the z-axis.
	twist_msg.angular.x = 0
	twist_msg.angular.y = 0
	twist_msg.angular.z = angle
	return twist_msg

# Calcua el angulo y la distancia que hay entre la meta y la tortuga, luego cambia el posición (angulo) de la tortuga hasta que el angulo sea cero o cercano a cero, finalmente mueve la tortuga hasta su posición final
def move(data, args):
	global pose

	goal = data
	rate = args[0]

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

		distance = get_distance(goal.x, goal.y)
		rospy.loginfo("distance %s", distance)

		if(pose.x > 9 or pose.x < 1 or pose.y > 9 or pose.y < 1):
			break

def listener():
    rospy.init_node('turtlesim_go_to_listener', anonymous=True)
    rate = rospy.Rate(0.5)
    rospy.Subscriber('turtlesim_go_to_talker', Pose, move, (rate,))
    rospy.Subscriber('turtle1/pose', Pose, get_position)
    rospy.spin()

if __name__ == '__main__':
    listener()
