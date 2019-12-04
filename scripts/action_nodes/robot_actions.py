#! /usr/bin/env python

"""
A collection of action nodes that publish commands to the Robot Arm Interface (tm).
"""

import rospy
import time
from action import Action
from std_msgs.msg import String

#commands= ["MANIP 1 \n","ARM 0 330 0 20 \n","MANIP 0 \n","MANIP 2 \n","ARM 0 0 60 20 \n"]
commands= ["MANIP 0 \n", "MANIP 1 \n", "MANIP 2 \n", "ARM 0 330 0 20 \n","ARM 0 0 60 20 \n"]

class OpenHandServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    self.pub = rospy.Publisher('armcommand', String, queue_size=10)

  def do_action(self):
    command = "MANIP 1 \n"
    print("publishing...")
    self.pub.publish(command)
    time.sleep(4)

class CloseHandServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    self.pub = rospy.Publisher('armcommand', String, queue_size=10)

  def do_action(self):
    command = "MANIP 0 \n"
    print("publishing...")
    self.pub.publish(command)
    time.sleep(4)