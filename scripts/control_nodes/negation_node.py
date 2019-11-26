#! /usr/bin/env python
import rospy

"""
todo: node that returns the negation of its child (like NOT)
"""

class NegationNode():

    def __init__(self, name):
        self.child = None
        self.name = name

    def tick(self):
        if self.child:
            status = self.child.tick()
            if status == "running":
                return status
            if status == "success":
                return "failure"
            if status == "failure":
                return "success"

    def reset(self):
        if self.child:
            self.child.reset()

    def add_child(self, node):
        self.child = node