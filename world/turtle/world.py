from sys import argv
# from maze import obstacles
import sandbox as obstacles
gui_loader = argv
gui_loader = [word.lower() for word in gui_loader]
gui_loader.append('turtle')
unit = 1.5
if 'turtle' in gui_loader:
    import turtle
    # import sandbox as obstacles


# tracking position
def world_pos_tracker(robot_name: str,turtle_variable):
    """
    tracks the x-axis and the y-axis position of the robot
    Then returns a message of the robots current position in the world

    Args:
        robot_name (str): The name of the robot
        turtle_variable : the turtle_name of the robot
        
    Returns:
        list: The robot's current position on the world map
        int : The robot's current degree of orientation
        string: message on the robots whereabouts
    """
    
    # retrieving the position of the turtle
    robot_position = turtle_variable.pos()
    # retrieves the degree that turtle is facing
    degree = turtle_variable.heading()
    
    # converting the returned float into int
    position = []
    for pos in robot_position:
        position.append(int(pos))
        
    # returning the message of the robots position 
    message = f" > {robot_name} now at position {tuple(position)}."
    return position,degree,message

def position_tracker(robot_name: str,coordinates: tuple,turtle_variable: object) -> str:
    """
    Updates the position of the robot in the world 
    By moving the turtle based off the values in the position tuple
    Args:
        turtle_variable (): the variable name of the turtle we wish to move
        position (list: Where we wish to move to

    Returns:
        _type_: _description_
    """

    x,y,degree = coordinates


    # The position the turtle must move to
    turtle_variable.goto(x*unit,y*unit)
    print(f" > {robot_name} now at position ({x},{y}).")
    return

def draw_borders(maze_height = 200 or int, maze_width = 100 or int):
    """
    Draws boundary lines for the robot. 
    The box restricts the robot movement.
    """
    

    # maze_height = maze_height / 2
    # maze_width = maze_width / 2
    
    
    # border settings
    border = turtle.Turtle()

    border.hideturtle()
    border.pen(pendown=False,pensize=3,speed=1000)

    # point at which we want to start drawing the boundary lines
    border.goto(maze_width * unit,-maze_height* unit)
    border.pendown()

    # drawing the right wall on the x-axis
    border.goto(maze_width* unit,maze_height* unit)
    
    # drawing the top wall on the y-axis
    border.goto(-maze_width*unit,maze_height* unit)
    
    # drawing the top wall on the y-axis
    border.goto(-maze_width* unit,-maze_height*unit)

    # drawing the bottom wall on the y-axis
    border.goto(maze_width*unit,-maze_height*unit)

# border patrol
def borders(command: list, degree: int,x: int,y: int,turtle_variable: object,maze_height: int = 200, maze_width: int = 100):
    """Sets a border and restricts how far the robot can actually in move a direction

    Args:
        command (list): command given to the robot
        degree (int): the direction the robot is facing
        x (int): The current position of the robot on the x-axis
        y (int): The current position of the robot on the y-axis

    Returns:
        bool: a True or False signal on whether the robot should move or not
    """
    position,degree,message = world_pos_tracker("",turtle_variable)
    x,y = position
    
    x_border, y_border = maze_width * unit, maze_height * unit
    neg_x_border, neg_y_border = -maze_width * unit, -maze_height * unit

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


# Turning mechanics

def direction_facing(degree: int, orientation: str,turtle_variable):
    """
    Controls the direction the robot faces using 90 degrees
    based of the given command from the user

    Args:
        degree (int): The current degrees the robot is facing
        orientation (str): Direction to turn (Left/Right)

    Returns:
        int : The new degrees that the robot is facing
    """

    # We use degrees to determine which direction the robot is facing (North, South , East, West)

    # For every time the user says right or left we add or minus 90 degrees to the robots current directional degree
    # In short at the start the robot is facing 0 degree, when we say right, he then turns 90 degrees

    # get the current degree that the robot is facing
    degree = turtle_variable.heading()
    
    if orientation == "Right":
        degree = degree - 90
    elif orientation == "Left":
        degree = degree + 90
    
    # change the robots's degree of orientation
    turtle_variable.setheading(degree)
    
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


def show_obstacles(obstacle_ref: list, cell_size: int = 4):
    """
    Hints to the user the coordinates of all
    the available obstacles in the world if any

    Args:
        obstacles_ref (list): a list of the available obstacles
        turtle_variable (object): Draws the obstacles in the world

    Returns:
        list : A list containing all the obstacles available in the world
    """

    # drawing the obstacle in the world
    # obstacle_list = obstacles.draw_obstacles(obstacle_ref,maze_height,maze_width,cell_size,color)
    print('There are some obstacles:')
    for obstacle in obstacle_ref:
        x,y = obstacle[0]
        print(f'- At position {x},{y} (to {x+cell_size},{y+cell_size})')

    return obstacle_ref


def is_blocked(robot_name: str,coordinates: tuple,obstacles_ref: list,command: list):
    x,y,degree = coordinates

    turns = ['Left','Right']
    if command[0] in turns:
        return False

    x1,y1 = obstacles.path_forecast(command,x,y,degree)
    if obstacles.is_path_blocked((x,y),(x1,y1),obstacles_ref):
        print(f'{robot_name}: Sorry, there is an obstacle in the way.')
        return True

    return False