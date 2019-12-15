# robot_behavior_trees
A package for python behavior trees integrated with ROS. Control and condition nodes are implemented as normal python classes, while action nodes are coded as action servers and are referenced through auxillary client nodes. To create your own action and condition nodes, create a new script in the actions or conditions folder and ensure your class(es) inherit from the general classes Action or Behavior.

Basic command parsing is also supported, with the main program being run in nlp_file_reader.py. It utilizes a modified shunting-yard algorithm to read pseudo-natural language from the example_behavior.txt file and automatically generates and executes the behavior tree specified. Subtasks can be temporarily abstracted away as subtrees using the "is" keyword. As of now, to hook up new nodes to the command parser:

    -import action and condition files at the top of the main file.
    -assign target keyword strings as word-split tuples in the global dictionary variable
    -assign instantiated action servers as values of action keys
    -assign instantiated condition nodes as values of condition keys
    
The command parser supports "and", "then", "or", "if", "repeat", and "is" keywords to assign action nodes and subtrees as children of control nodes. See examples for more information.

Currently, the main program can be called with rosrun campus_rover_behavior_trees nlp_file_reader.py. Ensure ROS is running with either gazebo or a live robot before executing.
