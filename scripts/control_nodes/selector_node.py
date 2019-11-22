#! /usr/bin/env python
import rospy

class SelectorNode():

    def __init__(self, name):
        self.children = []
        self.name = name

    def tick(self):
        #print("---" + self.name + "-->start")
        for node in self.children:
            child_status = node.tick()
            #print(node.name + " is " + child_status)
            if child_status == "running":
                #print("---" + self.name + "-->end")
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
            