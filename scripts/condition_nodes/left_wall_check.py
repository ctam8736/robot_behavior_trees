#! /usr/bin/env python

"""
Returns success tick if there is a wall to the robot's left.
"""

import rospy
from sensor_msgs.msg import LaserScan

class LeftWallCheckNode():

    def __init__(self, name):
        self.name = name
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.laser_cb)
        self.min_bearing_left = 5

    def laser_cb(self, msg):
        self.min_bearing_left = min(ranges[0:90])

    def tick(self):
        if self.min_bearing_left < .4:
            return "success"
        return "failure"

    def reset(self):
        pass