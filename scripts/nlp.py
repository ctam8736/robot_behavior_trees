#!/usr/bin/env python

"""
Modifiable command parser that asks for console input, constructs the corresponding behavior tree, and executes it.
"""

import rospy
import sys

from control_nodes import SequenceNode, SelectorNode, ParallelNode, RootNode, ClientNode
from action_nodes import twist_90, print_hello, navigate_rover
#from condition_nodes import

rospy.init_node('tree')

#init all keywords
dictionary = {("print", "hello"): print_hello.ActionServer('print_hello'),
              ("twist", "90"): twist_90.ActionServer('twist_90'),
              ("go", "to", "lab"): navigate_rover.ActionServer("go_to_lab"),
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
            if dictionary[tuple(last_phrase)]:
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