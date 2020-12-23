#!/usr/bin/env python

import rospy
from random import uniform
from std_msgs.msg import String
import json
from Crypto.Cipher import AES

key = 'BLhgpCL81fdLBk23HkZp8BgbT913cqt0'
iv = 'OWFJATh1Zowac2xr'
aes = AES.new(key, AES.MODE_CBC, iv)

def get_location():
    x = round(uniform(0, 11.09), 6)
    y = round(uniform(0, 11.09), 6)
    data = json.dumps({'x': x, 'y': y})

    if(len(data) < 32):
        n_pad = 32 - len(data)
        pad = ''
        for x in xrange(0,n_pad):
            pad += '0'
        data = data.replace('}', pad+'}')

    return aes.encrypt(data)

def talker():
    pub = rospy.Publisher('turtlesim_go_to_talker', String, queue_size=10)
    rospy.init_node('turtlesim_go_to_talker', anonymous=True)
    n = 0.05
    rate = rospy.Rate(n) 
    while not rospy.is_shutdown():
        data_message = get_location()
        pub.publish(data_message)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
