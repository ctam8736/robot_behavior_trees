#! /usr/bin/env python

"Sends a forward twist message to the robot when called."

import rospy
from action import Action

from geometry_msgs.msg import Twist

class ActionServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

  def do_action(self):
    move_twist = Twist()
    move_twist.linear.x = .2
    self.cmd_vel_pub.publish(move_twist)
