#! /usr/bin/env python

"""
A control node that ticks children sequentially, returning success tick only when all nodes return. (Can be thought of as an AND.)
"""

import rospy

class SequenceNode():

    def __init__(self, name):
        self.name = name
        self.children = []

    def tick(self):
        #print("---" + self.name + "-->start")
        for node in self.children:
            child_status = node.tick()
            #print(node.name + " is " + child_status)
            if child_status == "running":
                #print("---" + self.name + "-->end")
                return "running"
            elif child_status == "failure":
                print("---" + self.name + "-->failure")
                return "failure"
        print("---" + self.name + "-->success")
        return "success"

    def reset(self):
        for node in self.children:
            node.reset()

    def add_child(self, node):
        self.children.append(node)
            