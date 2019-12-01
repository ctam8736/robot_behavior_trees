#! /usr/bin/env python

"""
An auxillary node used to call action nodes indirectly.
"""

import rospy
import actionlib
from campus_rover_behavior_tree.msg import BTAction, BTGoal, BTFeedback, BTResult

class ClientNode():

    def __init__(self, name, param = None):
        self.name = name
        self.client = actionlib.SimpleActionClient(self.name, BTAction)
        self.client.wait_for_server()
        self.status = "idle"
        self.param = param

    def tick(self):
        if self.status is "idle":
            self.status = "running"
            goal = BTGoal()
            if self.param:
                goal.parameter = self.param
            self.client.send_goal(goal)
            return "running"
        elif self.status is "running":
            if self.client.get_result():
                return "success"
            return "running"

    def reset(self):
        self.status = "idle"