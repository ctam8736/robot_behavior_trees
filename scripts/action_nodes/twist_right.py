#! /usr/bin/env python

"""
Sends a clockwise Twist to the robot when called.
"""

import rospy
from geometry_msgs.msg import Twist

from action import Action

class ActionServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

  def do_action(self):
    turn_twist = Twist()
    turn_twist.angular.z = -.4
    self.cmd_vel_pub.publish(turn_twist)