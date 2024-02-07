# This module only contains the logic dynamics of how the robot moves
# when it is told to move

from world import world
import mechanics


def not_valid_for_movement(
    robot_name: str,
    command: str,
    x: int,
    y: int,
    degree: int,
    turtle_variable: object,
    obstacle,
) -> bool:
    """
    validates whether the given command is valid for movement

    Args:
        command (list: _description_

    Returns:
        bool : True if command is valid/False if otherwise
    """

    # checking whether the current steps that the robot is about to take is out of bounds or if the robot shall remain in the safe zone
    # If the move leads to the robot being out of bounds, a warning message is displayed to the user and the robot does not move even one step
    # test  step 10 left fw101
    if world.borders(command, degree, x, y, turtle_variable):
        print(world.safe_zone_warning(robot_name))
        return True

    if world.is_blocked(robot_name, (x, y, degree), obstacle, command):
        return True


def movement_logic(
    robot_name: str,
    command: list,
    x: int,
    y: int,
    degree: int,
    turtle_variable: object,
    obstacle: list,
):
    """
    Handles the 'Forward','Back' and 'Sprint' command logic
    when moving the robot based off the specified action

    Args:
        robot_name (str): The name of the robot
        command (list): The command given to the robot
        x (int): The position of the robot on the x-axis
        y (int): The position of the robot on the y-axis
        degree (int): The degree the robot is facing
        turtle_variable (object): The variable of the turtle we wish to move if playing the gui version
        obstacle (list): The coordinates of the obstacles in the world

    Returns:
        Tuple : tuple of arg x, y, degree, message, invalid_com
    """

    # if the command turns ot to be correct but it is missing a few parameters, it triggers the example
    invalid_com = False
    message = None  # if command is valid no error message

    # Checks the length of the forward command and ensures that the command has a length of 2
    if (len(command) != 2) or (not command[1].isdigit()):
        message = mechanics.command_example(command)
        invalid_com = True
        return x, y, degree, message, invalid_com

    if "Forward" in command:
        x, y, degree = forward_logic(
            robot_name, command, x, y, degree, turtle_variable, obstacle
        )
    elif "Back" in command:
        x, y, degree = back_logic(
            robot_name, command, x, y, degree, turtle_variable, obstacle
        )
    elif "Sprint" in command:
        x, y, degree = sprint_logic(
            robot_name, command, x, y, degree, turtle_variable, obstacle
        )

    return x, y, degree, message, invalid_com


def forward_logic(
    robot_name: str,
    command: str,
    x: int,
    y: int,
    degree: int,
    turtle_variable: object,
    obstacle,
):
    """
    Handle the moving forward logic based off the command given by the user
    Args:
        robot_name (str): The name of the robot
        command (str):The command given to the robot
        x (int): Position of the robot on x-axis
        y (int): Position of the robot on y-axis
        degree (int): The direction of orientation (dir robot is facing)
        history (list): The list of previously used commands by the user

    Returns:
        tuple : Returns a tuple of arg x,y,degree
    """
    # if the len of the command is correct and the argument (command[1]) is a digit
    # Before we execute the forward command, we must check the degree of orientation that the robot is facing
    # Then we move according to the direction that we are facing

    if not_valid_for_movement(
        robot_name, command, x, y, degree, turtle_variable, obstacle
    ):
        return x, y, degree

    if degree == 0:
        x = mechanics.forward_movement(robot_name, command[1], degree, x, y)

    elif degree == 90 or degree == -270:
        y = mechanics.forward_movement(robot_name, command[1], degree, x, y)

    elif degree == 180 or degree == -180:
        x = mechanics.forward_movement(robot_name, command[1], degree, x, y)

    elif degree == 270 or degree == -90:
        y = mechanics.forward_movement(robot_name, command[1], degree, x, y)

    return x, y, degree


def back_logic(
    robot_name: str,
    command: str,
    x: int,
    y: int,
    degree: int,
    turtle_variable: object,
    obstacle,
):
    """
    Handle the moving back logic based off the command given by the user
    Args:
        robot_name (str): The name of the robot
        command (str):The command given to the robot
        x (int): Position of the robot on x-axis
        y (int): Position of the robot on y-axis
        degree (int): The direction of orientation (dir robot is facing)
        history (list): The list of previously used commands by the user

    Returns:
        tuple : Returns a tuple of arg x,y,degree
    """

    # if the len of the command is correct and the argument (command[1]) is a digit
    if not_valid_for_movement(
        robot_name, command, x, y, degree, turtle_variable, obstacle
    ):
        return x, y, degree

    if degree == 0:
        x = mechanics.backwards_movement(robot_name, command[1], degree, x, y)

    elif degree == 90 or degree == -270:
        y = mechanics.backwards_movement(robot_name, command[1], degree, x, y)

    elif degree == 180 or degree == -180:
        x = mechanics.backwards_movement(robot_name, command[1], degree, x, y)

    elif degree == 270 or degree == -90:
        y = mechanics.backwards_movement(robot_name, command[1], degree, x, y)

    return x, y, degree


def sprint_logic(
    robot_name: str,
    command: str,
    x: int,
    y: int,
    degree: int,
    turtle_variable: object,
    obstacle,
):
    """
    Handle the moving sprinting logic based off the command given by the user
    Args:
        robot_name (str): The name of the robot
        command (str):The command given to the robot
        x (int): Position of the robot on x-axis
        y (int): Position of the robot on y-axis
        degree (int): The direction of orientation (dir robot is facing)
        history (list): The list of previously used commands by the user

    Returns:
        tuple : Returns a tuple of arg x,y,degree
    """

    # This list stores the number of strides per burst when the robot sprints
    strides_taken = []

    # if the len of the command is correct and the argument (command[1]) is a digit
    if not_valid_for_movement(
        robot_name, command, x, y, degree, turtle_variable, obstacle
    ):
        return x, y, degree

    if degree == 0:
        mechanics.sprinting(robot_name, command[1], degree, x, y, strides_taken)
        # The sum of the current_position_on(x/y) + sum_of_all_the_strides_taken (sum of all the values in the strides_list)
        x = x + sum(strides_taken)
        # Once we have added the sum of the strides to our (x/y) value, we empty the list for our next iteration
        del strides_taken[0:]

    elif degree == 90 or degree == -270:
        mechanics.sprinting(robot_name, command[1], degree, x, y, strides_taken)
        y = y + sum(strides_taken)
        del strides_taken[0:]

    elif degree == 180 or degree == -180:
        mechanics.sprinting(robot_name, command[1], degree, x, y, strides_taken)
        x = x - sum(strides_taken)
        del strides_taken[0:]

    elif degree == 270 or degree == -90:
        mechanics.sprinting(robot_name, command[1], degree, x, y, strides_taken)
        y = y - sum(strides_taken)
        del strides_taken[0:]

    return x, y, degree


def turn_logic(
    robot_name: str, command: list, x: int, y: int, degree: int, turtle_variable: object
):
    """Handles the logic of turning the robot left or right

    Args:
        robot_name (str): The name of the robot
        command (list): The command given to the robot
        x (int): Position on the x-axis
        y (int): Position on the y-axis
        degree (int): The directional degree that the robot is facing

    Returns:
        tuple : A tuple containing (x,y,degree)
    """

    invalid_com = False
    message = None

    if len(command) == 1:
        degree = world.direction_facing(degree, command[0], turtle_variable)
        degree = world.orientation_filter(degree)
        print(f" > {robot_name} turned {command[0].lower()}.")
    else:
        # if the command turns ot to be correct but it is missing a few parameters, it triggers the example
        message = f"Just type '{command[0].lower()}' to turn {command[0].lower()}."
        invalid_com = True

    return x, y, degree, message, invalid_com




