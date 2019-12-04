#!/usr/bin/env python

"""
Modifiable command parser that asks for console input, constructs the corresponding behavior tree, and executes it.
"""

import rospy
import sys
import json
from control_nodes import SequenceNode, SelectorNode, ParallelNode, RootNode, ClientNode, NavigationClientNode
from action_nodes import twist_90, print_hello, navigate_rover
from geometry_msgs.msg import Twist, Pose, Point, \
    Quaternion, PoseStamped, Transform, Vector3, TransformStamped
import os.path
#from condition_nodes import

rospy.init_node('tree')

"""
with open(os.path.dirname(__file__) + '/../info/basement_demo_waypoints.json') as json_file:
    #data = json.load(json_file)
    for key in json.load(json_file):
        print(key)
"""

#init temporary coordinates
lab_coordinates = PoseStamped()
lab_coordinates.pose.position.x = 19.0380267163
lab_coordinates.pose.position.y = 20.7569543047
lab_coordinates.pose.position.z = 0.0
lab_coordinates.pose.orientation.x = 0.0
lab_coordinates.pose.orientation.y = 0.0
lab_coordinates.pose.orientation.z = -0.211043131282
lab_coordinates.pose.orientation.w = 0.977476749973

#init all keywords
dictionary = {("print", "hello"): print_hello.ActionServer('print_hello'),
              ("twist", "90"): twist_90.ActionServer('twist_90'),
              ("go", "to", "lab"): lab_coordinates,
              ("and", ): None,
              ("or", ): None,
              ("then", ): None
              }



#handle the next operation given value and op stack
def apply_op(operators, values):
    operator = operators.pop()
    node = None
    #handle binary operations
    if operator == "and" or operator == "or" or operator == "then":
        if operator == "and":
            node = ParallelNode("dummy", 2, 2)
        elif operator == "or":
            node = SelectorNode("dummy")
        elif operator == "then":
            node = SequenceNode("dummy")
        right = values.pop()
        left = values.pop()
        node.add_child(left)
        node.add_child(right)
        values.append(node)

#parses console input and adds computed behavior tree to root
def construct_tree(command):
    global dictionary, root

    last_phrase = []

    #perform basic shunting yard
    values = []
    operators = []
    for i in range(len(command)):
        last_phrase.append(command[i])
        print(last_phrase)
        #terminate keyword
        if last_phrase[0] == "exit":
            rospy.signal_shutdown("Console terminated.")
        #recognize if string is a command or keyword I know
        if tuple(last_phrase) in dictionary:
            reference = dictionary[tuple(last_phrase)]
            print(type(reference))
            if isinstance(reference, PoseStamped):
                #navigation action
                values.append(NavigationClientNode("_".join(last_phrase), reference))
                print("_".join(last_phrase) + " was recognized.")
            elif reference:
                #normal action
                values.append(ClientNode("_".join(last_phrase)))
                print("_".join(last_phrase) + " was recognized.")
            else:
                operators.append("".join(last_phrase))
                print("".join(last_phrase) + " was recognized.")
            last_phrase = []
        #added: check repeater arguments
        if len(last_phrase) == 2 and unicode(last_phrase[0]).isnumeric() and last_phrase[1] == "times":
            old = values.pop()
            values.append(ClientNode(old.name, param = int(last_phrase[0])))
            last_phrase = []
    if not last_phrase:
        #apply operators
        while len(operators) > 0:
            apply_op(operators, values)
        #finished behavior tree is the last in the stack
        if values:
            root.add_child(values.pop())
        return True
    else:
        #command was not completely keywords
        print("Command failed to parse completely.")
        return False

#console loop, tick root until success
while not rospy.is_shutdown():

    root = RootNode('root')
    
    command = raw_input("Enter command: ").split()

    if construct_tree(command):
        status = root.tick()
        while not status is "success":
            status = root.tick()
        print(root.name + " is " + status + ".")