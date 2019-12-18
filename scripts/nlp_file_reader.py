#!/usr/bin/env python

"""
Modifiable command parser that reads in the file example_behavior.txt, constructs the corresponding behavior trees, and executes the last root.
"""

from __future__ import print_function
import rospy
import sys
import json
from control_nodes import SequenceNode, SelectorNode, ParallelNode, RootNode, ClientNode, NavigationClientNode, RepeaterNode
from action_nodes import twist_90, print_hello, navigate_rover, robot_actions, movement_actions
from condition_nodes import condition, wall_check
from geometry_msgs.msg import Twist, Pose, Point, \
    Quaternion, PoseStamped, Transform, Vector3, TransformStamped
import os

#print(os.listdir('/home/robotics/catkin_ws/src/campus_rover_behavior_tree/scripts/example_behavior.txt'))

rospy.init_node('tree')

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
              ("open", "hand"): robot_actions.OpenHandServer('open_hand'),
              ("close", "hand"): robot_actions.CloseHandServer('close_hand'),
              ("retract", "arm"): robot_actions.RetractArmServer('retract_arm'),
              ("move", "forward"): movement_actions.MoveForwardServer('move_forward'),
              ("move", "backward"): movement_actions.MoveBackwardServer('move_backward'),
              ("turn", "right"): movement_actions.TurnRightServer('turn_right'),
              ("turn", "left"): movement_actions.TurnLeftServer('turn_left'),

              ("wall", "in", "front"): wall_check.WallCheckNode('wall_in_front'),

              ("and", ): None,
              ("or", ): None,
              ("then", ): None,
              ("repeat", ): None,
              ("if", ): None,
              }

#handle the next operation given value and op stack
def apply_op(operators, values):
    operator = operators.pop()
    node = None
    #handle binary operations
    if operator == "and" or operator == "or" or operator == "then" or operator == "if":
        if operator == "and":
            node = ParallelNode("parallel", 2, 2)
            print("-->Instatiating parallel node with children: ", end="")
        elif operator == "or":
            node = SelectorNode("selector")
            print("-->Instatiating selector node with children: ", end="")
        elif operator == "then" or operator == "if":
            node = SequenceNode("sequence")
            print("-->Instatiating sequence node with children: ", end="")
        right = values.pop()
        left = values.pop()
        print(left.name + ", " + right.name)
        node.add_child(left)
        node.add_child(right)
        values.append(node)
    if operator == "repeat":
        child = values.pop()
        node = RepeaterNode("repeater")
        node.add_child(child)
        values.append(node)

#parses console input and adds computed behavior tree to root
def construct_tree(command):
    global dictionary
    root = RootNode('root')
    assignee = None
    last_phrase = []
    #perform basic shunting yard
    values = []
    operators = []
    for i in range(len(command)):
        last_phrase.append(command[i])
        #terminate keyword
        if last_phrase[0] == "exit":
            rospy.signal_shutdown("Console terminated.")
        #recognize if string is a command or keyword I know
        if tuple(last_phrase) in dictionary:
            reference = dictionary[tuple(last_phrase)]
            if isinstance(reference, PoseStamped):
                #navigation action
                values.append(NavigationClientNode("_".join(last_phrase), reference))
                print("_".join(last_phrase) + " was recognized.")
            elif isinstance(reference, RootNode) or isinstance(reference, wall_check.WallCheckNode):
                #handle remembered action or condition
                values.append(reference)
                print("_".join(last_phrase) + " was recognized.")
            elif reference:
                #normal action
                values.append(ClientNode("_".join(last_phrase)))
                print("_".join(last_phrase) + " was recognized.")
            else:
                operators.append("".join(last_phrase))
                print("_".join(last_phrase) + " was recognized.")
            last_phrase = []
        #added: check repeater arguments
        if len(last_phrase) == 2 and unicode(last_phrase[0]).isnumeric() and last_phrase[1] == "times":
            old = values.pop()
            values.append(ClientNode(old.name, param = int(last_phrase[0])))
            last_phrase = []
        #added: check assignment
        if last_phrase and last_phrase[-1] == "is":
            assignee = last_phrase[:-1]
            last_phrase = []
    if not last_phrase:
        #apply operators
        while len(operators) > 0:
            apply_op(operators, values)
        #finished behavior tree is the last in the stack
        if values:
            root.add_child(values.pop())
            #remember root if assignment
            if assignee:
                root.name = "_".join(assignee)
                dictionary[tuple(assignee)] = root
                print("Task " + str(tuple(assignee)) + " remembered.")
                return None
        return root
    else:
        #command was not completely keywords
        print("Command failed to parse completely.")
        return None

commands = []
with open('/home/robotics/catkin_ws/src/campus_rover_behavior_tree/scripts/example_behavior.txt', 'r') as f:
    for line in f:
        commands.append(line.split())

for command in commands:
    root = construct_tree(command)
    if root:
        print("END FILE PARSE. EXECUTING BEHAVIOR TREE.")
        status = root.tick()
        while not status is "success":
            status = root.tick()
        print(root.name + " is " + status + ".")

"""
#console loop, tick root until success
while not rospy.is_shutdown():
    root = RootNode('root')
    command = raw_input("Enter command: ").split()
    if construct_tree(command):
        status = root.tick()
        while not status is "success":
            status = root.tick()
        print(root.name + " is " + status + ".")
"""