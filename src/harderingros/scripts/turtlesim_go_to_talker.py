import rospy
from random import uniform
from turtlesim.msg import Pose

def talker():
    pub = rospy.Publisher('turtlesim_go_to_talker', Pose, queue_size=10)
    rospy.init_node('turtlesim_go_to_talker', anonymous=True)
    rate = rospy.Rate(0.1) # 10hz
    while not rospy.is_shutdown():
        pose_message = get_location()
        rospy.loginfo(pose_message)
        pub.publish(pose_message)
        rate.sleep()

def get_location():
    pose = Pose()
    pose.x = uniform(0, 11.0) 
    pose.y = uniform(0, 11.0) 
    pose.theta = 0.0
    pose.linear_velocity = 0.0
    pose.angular_velocity = 0.0
    return pose

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
