#! /usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from condition import Condition

"""
Returns success tick if there is a wall in front of the robot.
"""

class WallCheckNode(Condition):

    def __init__(self, name):
        Condition.__init__(self, name)
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.laser_cb)
        self.bearing_zero = 5

    def laser_cb(self, msg):
        self.bearing_zero = msg.ranges[0]

    def check(self):
        return self.bearing_zero < .6