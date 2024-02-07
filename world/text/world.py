from maze import obstacles

# tracking position
def position_tracker(robot_name: str,coordinates: tuple,turtle_variable: object) -> str:
    """
    tracks the x-axis and the y-axis position of the robot
    Then Prints a message of the robots current position on the axises

    Args:
        robot_name (str): Name of the robot
        x (int): the x axis of the robot
        y (int): the y axis of the robot
    """

    x,y,degree = coordinates

    # The position the robot is
    print(f" > {robot_name} now at position ({x},{y}).")
    return

# border patrol
def borders(command: list, degree: int, x: int, y: int,turtle_variable: object, maze_height: int = 200, maze_width: int = 100):
    """Sets a border and restricts how far the robot can actually in move a direction

    Args:
        command (list): command given to the robot
        degree (int): the direction the robot is facing
        x (int): The current position of the robot on the x-axis
        y (int): The current position of the robot on the y-axis

    Returns:
        bool: a True or False signal on whether the robot should move or not
    """

    x_border, y_border = maze_width, maze_height
    neg_x_border, neg_y_border = -maze_width, -maze_height

    # initially the limit reached switch is false and if it remains false then the robot shall proceed in the desired direction
    limit_reached = False

    # limit is the sum of the robots current position and the number of steps the robot needs to take
    # limit = current_position_on(x/y) +/- number_of_steps_to_move
    limit = safety_zone(degree, command, x, y)
    # if the value of limit is within the safe zone range and limit reached remains false
    # if the value of limit is greater than the values of the set borders, the limit_reached variable becomes true
    
    # We start off by checking which direction the robot is facing and then we check which command is being given to the robot
    if degree == 0:
        if (command[0] == "Forward" or command[0] == "Sprint") and (limit > x_border or limit < neg_x_border):
            limit_reached = True
        elif (command[0] == "Back") and (limit < neg_x_border or limit > x_border):
            limit_reached = True

    elif degree == 90 or degree == -270:
        if (command[0] == "Forward" or command[0] == "Sprint") and (limit < neg_y_border or limit > y_border):
            limit_reached = True
        elif (command[0] == "Back") and (limit < neg_y_border or limit > y_border):
            limit_reached = True

    elif degree == 180 or degree == -180:
        if (command[0] == "Forward" or command[0] == "Sprint") and (limit < neg_x_border or limit > x_border):
            limit_reached = True
        elif (command[0] == "Back") and (limit < neg_x_border or limit > x_border):
            limit_reached = True

    elif degree == 270 or degree == -90:
        if (command[0] == "Forward" or command[0] == "Sprint") and (limit < neg_y_border or limit > y_border):
            limit_reached = True
        elif (command[0] == "Back") and (limit < neg_y_border or limit > y_border):
                limit_reached = True

    return limit_reached


def safety_zone(degree: int, command: list, x: int, y: int):
    """Returns a sum of the robots current position + the number of steps the robot needs to take

    Args:
        degree (int): The direction the robot is facing in degrees
        command (list): The command given to the robot
        x (int): The current number of steps on the x-axis
        y (int): The current number of steps on the y-axis

    Returns:
        _int_: the sum of the steps
    """

    steps = int(command[1])

    # Before we do anything we are always checking which direction the robot is facing then which command is being given to the robot
    if degree == 0:
        # Based off the command that is being given to the robot we return an int value of the sum of the the robots current_steps_on(x/y) + number_of_steps_to_take
        if "Forward" in command or "Sprint" in command:
            limit = x + steps
        elif "Back" in command:
            limit = x - steps

    elif degree == 90 or degree == -270:
        if "Forward" in command or "Sprint" in command:
            limit = y + steps
        elif "Back" in command:
            limit = y - steps

    elif degree == 180 or degree == -180:
        if "Forward" in command or "Sprint" in command:
            limit = x - steps
        elif "Back" in command:
            limit = x + steps

    elif degree == 270 or degree == -90:
        if "Forward" in command or "Sprint" in command:
            limit = y - steps 
        elif "Back" in command:
            limit = y + steps

    # The returned sum is based off the command and the robots direction of orientation (the direction the robot is facing)
    return limit


def safe_zone_warning(robot_name: str):
    """
    Warns the user if the specified number of steps takes the robot beyond the set borders
    """
    return (f"{robot_name}: Sorry, I cannot go outside my safe zone.")

# orientation logic (turning)
def direction_facing(degree: int, orientation: str,turtle_variable = None):
    """Controls the direction the robot faces by adjusting the degrees accordingly

    Args:
        degree (int): The current degrees the robot is facing
        orientation (str): Direction to turn (Left/Right)

    Returns:
        int : The new degrees that the robot is facing
    """

    # We use degrees to determine which direction the robot is facing (North, South , East, West)

    # For every time the user says right or left we add or minus 90 degrees to the robots current directional degree
    # In short at the start the robot is facing 0 degree, when we say right, he then turns 90 degrees

    if orientation == "Right":
        degree = degree - 90
    elif orientation == "Left":
        degree = degree + 90

    return degree


def orientation_filter(degree: int):
    """Limits the robot from rotating more than a single revolution either side (max rotation = -360/360)

    Args:
        degree (int): Current rotational degree

    Returns:
        int : The adjusted rotational degree
    """

    # In the event where the robots rotates s more than 360 degrees, we need to reset its degrees clock back to 0
    # This prevents the robot from rotating more than a single revolution thus we stick between 0 and 360 degrees
    if degree >= 360 or degree <= -360:
        degree = 0
  
    # If the rotational degree is more than 360 we shall return 0 , or else we will return its unchanged degree
    # Example if the degree is 90 we will return 90 if its 450 we will return 0

    return degree



def show_obstacles(obstacle_ref: list,cell_size: int = 4):
    """
    Hints to the user the coordinates of all
    the available obstacles in the world if any

    Args:
        obstacles (list): a list of the available obstacles
        turtle_variable (object): Draws the obstacles in the world
        
    Returns:
        list: A list of all the obstacle sin the world 
    """

    print('There are some obstacles:')
    for obstacle in obstacle_ref:
        x,y = obstacle[0]
        print(f'- At position {x},{y} (to {x + cell_size},{y + cell_size})')
    
    return obstacle_ref


def is_blocked(robot_name: str,coordinates: tuple,obstacles_ref: list,command: list):
    """
    Checks whether the position that the robot is heading to is blocked

    Args:
        robot_name (str): The name of the robot
        coordinates (tuple): The degree the robot is facing, and its position on the x/y axis
        obstacles_ref (list): The coordinates to all the obstacles
        command (list): The command being given to the robot

    Returns:
        bool: True/False if the position is blocked/not blocked
    """
    x,y,degree = coordinates

    turns = ['Left','Right']
    if command[0] in turns:
        return False

    x1,y1 = obstacles.path_forecast(command,x,y,degree)
    if obstacles.is_path_blocked((x,y),(x1,y1),obstacles_ref):
        print(f'{robot_name}: Sorry, there is an obstacle in the way.')
        return True

    return False