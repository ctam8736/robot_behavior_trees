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

"""
todo: node that keeps calling child after success is returned, else returns failure
"""

class RepeaterNode():

    def __init__(self, name):
        self.child = None
        self.name = name

    def tick(self):
        if self.child:
            status = self.child.tick()
            if status == "failure":
                return "failure"
            if status == "success":
                self.reset()
                self.child.tick()
                print("repeating---")
            return "running"

    def reset(self):
        if self.child:
            self.child.reset()

    def add_child(self, node):
        self.child = node