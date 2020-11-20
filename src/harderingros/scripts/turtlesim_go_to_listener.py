import rospy
from turtlesim.msg import Pose

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)

def turtlesim_go_to_listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('turtlesim_go_to_talker', Pose, callback)
    rospy.spin()

if __name__ == '__main__':
    turtlesim_go_to_listener()
