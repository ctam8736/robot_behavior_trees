#!/usr/bin/env python

"""
Modifiable command parser that asks for console input, constructs the corresponding behavior tree, and executes it.
"""

import rospy

from control_nodes import SequenceNode, SelectorNode, ParallelNode, RootNode, ClientNode
from action_nodes import twist_90, print_hello
#from condition_nodes import

rospy.init_node('tree')
dictionary = {("print", "hello"): print_hello.ActionServer('print_hello'),
              ("twist", "90"): twist_90.ActionServer('twist_90')}


def apply_op(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    node = None
    if operator == "and":
        node = ParallelNode("dummy", 2, 2)
    elif operator == "or":
        node = SelectorNode("dummy")
    elif operator == "then":
        node = SequenceNode("dummy")
    node.add_child(left)
    node.add_child(right)
    values.append(node)

while not rospy.is_shutdown():

    root = RootNode('root')

    #get input      
    command = raw_input("Enter command: ").split()
    last_phrase = []

    #perform basic shunting yard
    values = []
    operators = []
    for word in command:
        if word == "and" or word == "or" or word == "then":
            last_phrase = []
            operators.append(word)
        else:
            last_phrase.append(word)
            if tuple(last_phrase) in dictionary:
                values.append(ClientNode("_".join(last_phrase)))
                print("_".join(last_phrase) + " was recognized.")
                last_phrase = []

    while len(operators) > 0:
        apply_op(operators, values)
    if values:
        root.add_child(values.pop())

    status = root.tick()
    while not status is "success":
        status = root.tick()
        pass
    print(root.name + " is " + status + " and resetting.")

    """
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        status = root.tick()
        if status is "success":
            print(root.name + " is " + status + " and resetting.")
            root.reset()
        rate.sleep()
    """