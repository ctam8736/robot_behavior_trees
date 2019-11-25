#! /usr/bin/env python

"""
Prints hello to console 10 times when called.
"""

import rospy
from action import Action

class ActionServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)

  def do_action(self):
    rate = rospy.Rate(3)
    for i in range(10):
      print("Hello!")
      rate.sleep()