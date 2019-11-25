#! /usr/bin/env python

"""
Returns success tick if there is a wall to the robot's right.
"""

import rospy
from sensor_msgs.msg import LaserScan

class RightWallCheckNode():

    def __init__(self, name):
        self.name = name
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.laser_cb)
        self.min_bearing_right = 5

    def laser_cb(self, msg):
        self.min_bearing_right = min(ranges[270:])

    def tick(self):
        if self.min_bearing_right < .4:
            return "success"
        return "failure"

    def reset(self):
        pass