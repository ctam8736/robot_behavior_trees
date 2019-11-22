#! /usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan

class WallCheckNode():

    def __init__(self, name):
        self.name = name
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.laser_cb)
        self.bearing_zero = 5

    def laser_cb(self, msg):
        self.bearing_zero = msg.ranges[0]

    def tick(self):
        if self.bearing_zero < .6:
            return "success"
        return "failure"

    def reset(self):
        pass