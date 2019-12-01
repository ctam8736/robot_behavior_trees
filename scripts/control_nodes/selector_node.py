#! /usr/bin/env python

"""
A control node that ticks children sequentially, returning success tick when a single node returns success. (Can be thought of as an OR.)
"""

import rospy

class SelectorNode():

    def __init__(self, name):
        self.children = []
        self.name = name

    def tick(self):
        for node in self.children:
            child_status = node.tick()
            if child_status == "running":
                return "running"
            elif child_status == "success":
                print("---" + self.name + "-->success")
                return "success"
        print("---" + self.name + "-->failure")
        return "failure"

    def reset(self):
        for node in self.children:
            node.reset()

    def add_child(self, node):
        self.children.append(node)
            