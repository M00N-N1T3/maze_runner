# This module does all the heavy lifting
# it handles the mechanics of how the robot moves and navigates the world

def forward_movement(robot_name: str, steps: str, degree: int, x: int, y: int):
    """
    Controls the forward direction that the robot moves based of its degree of orientation
    270 / - 90 is North
    90 / - 270 is South
    0 / 360 is East
    180 / -180 is West

    Args:
        robot_name (str): The name of the robot
        steps (str): The number of steps the robot should move
        degree (int): The direction the robot is facing
        x (int): The total of steps the robot has moved on the x-axis
        y (_type_): The total of steps the robot has moved on the y-axis

    Returns:
        int : The number of steps the robot should move based of their orientation
    """
    # The number of steps the robot takes is converted to an int
    steps = int(steps)
    print(f" > {robot_name} moved forward by {steps} steps.")

    # Then we check what is the current degree that the robot is facing
    # Based of the degree the robot is facing we will move the robot forward accordingly
    if degree == 0:
        move_by = x + steps 
    elif degree == 90 or degree == -270:
        move_by = y + steps 
    elif degree == 180 or degree == -180:
        move_by = x - steps
    elif degree == 270 or degree == -90:
        move_by = y - steps 

    # The amount of steps the robot should move by
    return move_by


def backwards_movement(robot_name: str, steps: str, degree: int, x: int, y: int):
    """
    Controls the backwards direction that the robot moves based of its degree of orientation
    270 / - 90 is North
    90 / - 270 is South
    0 is East
    180 / -180 is West

    Args:
        robot_name (str): The name of the robot
        steps (str): The number of steps the robot should move
        degree (int): The direction the robot is facing
        x (int): The total of steps the robot has moved on the x-axis
        y (_type_): The total of steps the robot has moved on the y-axis

    Returns:
        int : The number of steps the robot should move based of their orientation
    """

    # The number of steps the robot takes is converted to an int
    steps = int(steps)
    print(f" > {robot_name} moved back by {steps} steps.")

    # Then we check what is the current degree that the robot is facing
    # Based of the degree the robot is facing we will move the robot backwards accordingly
    # moving backwards is a direct inverse of my move_forward function
    if degree == 0:
        move_by = x - steps 
    elif degree == 90 or degree == -270:
        move_by = y - steps # switched + to -
    elif degree == 180 or degree == -180:
        move_by = x + steps
    elif degree == 270 or degree == -90:
        move_by = y + steps # switched - to +

    # Returning the number of steps the robot should move back by
    return move_by


def sprinting(robot_name, stride, degree, x, y, stride_tracker):
    """
    Controls the sprint mechanics of the robot.
    The robot sprints by bursting in the from of the sum of steps taken per stride.
    Thus a sprint of 5 is 5 + 4 + 3 + 2 + 1

    Args:
        robot_name (str): The name of the robot
        stride (int): How far the robot should sprint
        degree (int): The robots current orientation (the direction the robot is facing)
        x (int): The robots current position on the x-axis
        y (int): The robots current position on the y-axis

    Returns:
        int : the number of steps the robot moved
    """

    # Strides is how many steps the robot takes per burst. Consider it as the robots rpm
    stride = int(stride)

    # My base case. It ends our recursive loop as soon as the robot takes its last stride step
    if stride == 1:
        # For every base step completion the number of strides taken by the robot gets appended to an external stride tracker list
        forward_movement(robot_name, stride, degree, x, y)
        return stride_tracker.append(stride)
    else:
        # The current amount of strides that needs to be taken on this burst call is appended to the list of previous
        stride_tracker.append(stride)
        forward_movement(robot_name, stride, degree, x, y)
        return sprinting(robot_name, stride - 1, degree, x, y, stride_tracker)

# Examples/Messages for user
def command_example(command):
    """Prints an example of how to use the command for the user

    Args:
        command (str): The command inputted by the user
    """
    # The message that is printed to the user on how to use the command
    return (f"Specify number of steps in digits (Example: {command[0].lower()} 10).")