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
    rate = rospy.Rate(5)
    print("Hello!")
    rate.sleep()

  def execute_cb(self, goal):
    rate = rospy.Rate(10)
    success = True
    if goal.parameter:
      for i in range(goal.parameter):
        self.do_action()
    else:
      for i in range(10):
        self.do_action()
    if success:
      self.set_status('SUCCESS')