#! /usr/bin/env python

"""
A general action node class that instantiates a customizable action server for client nodes.
"""

import rospy
import actionlib
from campus_rover_behavior_tree.msg import BTAction, BTGoal, BTFeedback, BTResult

class Action:
    _feedback = BTFeedback()
    _result   = BTResult()

    def __init__(self, name):
        self.name = name
        self._as = actionlib.SimpleActionServer(self.name, BTAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()

    def execute_cb(self, goal):
        rate = rospy.Rate(10)
        success = True
        self.do_action()
        if success:
            self.set_status('SUCCESS')

    def set_status(self,status):
        if status == 'SUCCESS':
            self._feedback.status = 1
            self._result.status = self._feedback.status
            self._as.set_succeeded(self._result)
        elif status == 'FAILURE':
            self._feedback.status = 2
            self._result.status = self._feedback.status
            self._as.set_succeeded(self._result)
        else:
            pass
    
    def do_action(self):
        pass