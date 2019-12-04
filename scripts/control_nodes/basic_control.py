#! /usr/bin/env python

import rospy

"""
A node to be designated as the root of a behavior tree, with only one child.
"""

class RootNode():

    def __init__(self, name):
        self.child = None
        self.name = name

    def tick(self):
        if self.child:
            return self.child.tick()

    def reset(self):
        if self.child:
            self.child.reset()

    def add_child(self, node):
        self.child = node

"""
A control node that ticks children sequentially, returning success tick only when all nodes return. (Can be thought of as an AND.)
"""

class SequenceNode():

    def __init__(self, name):
        self.name = name
        self.children = []

    def tick(self):
        for node in self.children:
            child_status = node.tick()
            if child_status == "running":
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

"""
A control node that ticks children sequentially, returning success tick when a single node returns success. (Can be thought of as an OR.)
"""

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

"""
A control node that ticks children in parallel/synchronously. Returns success or failure based on input thresholds.
"""

class ParallelNode():

    def __init__(self, name, ns, nf):
        self.children = []
        self.ns = ns
        self.nf = nf
        self.name = name

    def tick(self):
        s = 0
        f = 0
        for i, node in enumerate(self.children):
            child_status = node.tick()
            if child_status == "success":
                s = s + 1
            elif child_status == "failure":
                f = f + 1
        if s >= self.ns:
            return "success"
        if f >= self.nf:
            return "failure"
        return "running"

    def reset(self):
        for node in self.children:
            node.reset()

    def add_child(self, node):
        self.children.append(node)
            