import random
from sys import argv

# display unit increases the graphics, easier on the eyes
unit = 1

gui_loader = argv
gui_loader = [word.lower() for word in gui_loader]

if 'turtle' in gui_loader:
    import turtle

# creating obstacles
# in the text world, the obstacle is a tuple containing 4 tuple elements
def create_obstacle(xcord: int = 100, ycord: int = 200, cell_size: int = 4) -> tuple:
    """
    creates the obstacles within our world
    The obstacle is a 4 by 4 square.
    Each corner of the square contains an (x,y) coordinate
    corner 1 = (x,y) | 2 = (x+4,y) | 3 = (x+4,y+4) | 4 = (x,y+4)

    Returns:
        list :a list containing the 4 point of the obstacle
    """
    # point 1 = (x,y)       point 2 = (x+4,y)
    #         |---------------------|
    #         | pretend its 4 x 4   |
    #         |---------------------|
    # point 4 = (x,y+4)     point 3 = (x+4,y+4)
    
    # temporary list to store an obstacle
    obstacle = list()
    
    # # ensuring that neither x or y is = 0, as that is our spawn point
    
    try:
        xcord = random.randint(-xcord,xcord)
        ycord = random.randint(-ycord,ycord)
    except ValueError:
        xcord = random.randint(-100,100)
        ycord = random.randint(-200,200)
            

    
    
    # creating our 4 by 4 square 
    obstacle.append((xcord,ycord))
    obstacle.append((xcord+cell_size,ycord))
    obstacle.append((xcord+cell_size,ycord+cell_size))
    obstacle.append((xcord,ycord+cell_size))

    return tuple(obstacle)

def generate_obstacles(height=200 , width= 100, cell_size = 4):
    """
    Generates a  list of obstacles
    each obstacle is a tuple with a set of 4 tuples containing (x,y) coordinates
    The set of 4 tuples, together create a 4 by 4 square (the obstacle)

    Returns:
        list : a list of all the available obstacles in the world
    """
    exits = None
    gui_loader = argv
    gui_loader = [word.lower() for word in gui_loader]
    # see if this is simple or mad man maze to be fair I think its simple
    obstacles = [create_obstacle(width,height,cell_size) for i in range (random.randint(0,10))]
    
    # it will only draw the obstacles if we running in gui 
    if 'turtle' in gui_loader:
        draw_obstacles(obstacles,height,width,cell_size,'black')

    return obstacles , exits, None, None

def draw_obstacles(obstacles: list|tuple,maze_height: int = 204 , maze_width: int = 104, cell_size: int = 4 , color:  str = 'white' ):
    """
    Draws a visual representation of the obstacles within the turtle realm

    Args:
        obstacles (list): a list containing the coordinates of the obstacles

    Returns:
        list: A list of all the obstacles drawn
    """
    # if the user does not give us a list of the coordinates of the obstacles
    # we randomly generate one fo them
    if obstacles == "" or not isinstance(obstacles,list) or len(obstacles) <1:
        return


    # drawing the obstacles
    drawer = turtle.Turtle()
    drawer.hideturtle()
    turtle.tracer(0)
    

    for obstacle in obstacles:
        x,y = obstacle[0]
        drawer.penup()
        drawer.goto(x*unit,y * unit)
        drawer.begin_fill()
        drawer.pen(pendown=False,fillcolor=color,speed=0)
        for co in reversed(obstacle):
            z,y = co
            drawer.goto(z*unit,y*unit)
        drawer.end_fill()

    turtle.tracer(1)

    return obstacles


def is_path_blocked(position1: tuple,position2: tuple,obstacles: list) -> bool:
    """
    Checks whether the path from point A to point B is blocked by an obstacle
    Example : if the robot wants to move from (10,19) to (14,19), we will check
    whether there is an obstacle in that path, which restrict movement

    Args:
        position1 (tuple): A tuple of the (x,y) coordinates that the robot is at (where it is standing)
        position2 (tuple): A tuple of the (x,y) coordinates that the robot will end up at if it moves
        obstacles (list): A list containing all the obstacles in the world

    Returns:
        bool : True if there is an object in the path  / False if there is no object in the path
    """
    # point 1 = (x,y)       point 2 = (x+4,y)
    #         |---------------------|
    # (x1,y1) | pretend its 4 x 4   | (x2,y2)
    #         |---------------------|
    # point 4 = (x,y+4)     point 3 = (x+4,y+4)

    x1,y1= position1
    x2,y2 = position2


    if x1 == x2:
        if is_position_blocked(x1,y2,obstacles):
            return True
    elif y1 == y2:

        if is_position_blocked(x2,y1,obstacles):
            return True

    return False



def is_position_blocked(x,y,obstacles: list) -> bool:
    """
    Checks whether there is an obstacle in the position that the robot
    wants to move to, before it moves the robot
    Example : if the robot wants to move to (10,19), we will check
    if there is any object at position (10,19)

    Args:
        position (tuple): A tuple of the (x,y) coordinates that want the robot ot move to

        obstacles (list): A list containing all the obstacles in the world

    Returns:
        bool : True if there is an object in  / False if there is no object that position
    """
    # point 1 = (x,y)       point 2 = (x+4,y)
    #         |---------------------|
    #         | pretend its 4 x 4   |
    #         |---------------------|
    # point 4 = (x,y+4)     point 3 = (x+4,y+4)

    # line 1: x to x+4
    # line 2: y to y+4
    # line 3: x to x+4
    # line 2: y to y+4

    for obstacle in obstacles:

        x1,y1 = obstacle[0]


        for numx in range(x1-4,x1):
            if x == int(numx):

                for numy in range(y1,y1+4):
                    if y == int(numy):
                        return True

    
    return False


def path_forecast(command:list, x:int ,y:int,degree: int) -> tuple:

    """Predicts the robots next positional coordinates
    if it was to move from its current position to its next position

    Args:
        degree (int): The direction the robot is facing in degrees
        command (list): The command given to the robot
        x (int): The current number of steps on the x-axis
        y (int): The current number of steps on the y-axis

    Returns:
        tuple : A forecast of what the robot's new coordinations will be
    """   
    steps = int(command[1])

    # Before we do anything we are always checking which direction the robot is facing then which command is being given to the robot
    if degree == 0:
        # Based off the command that is being given to the robot we return an int value of the sum of the the robots current_steps_on(x/y) + number_of_steps_to_take
        if "Forward" in command or "Sprint" in command:
            x = x + steps
        elif "Back" in command:
            x = x - steps

    elif degree == 90 or degree == -270:
        if "Forward" in command or "Sprint" in command:
            y = y + steps
        elif "Back" in command:
            y = y - steps

    elif degree == 180 or degree == -180:
        if "Forward" in command or "Sprint" in command:
            x = x - steps
        elif "Back" in command:
            x = x + steps

    elif degree == 270 or degree == -90:
        if "Forward" in command or "Sprint" in command:
            y = y - steps
        elif "Back" in command:
            y = y + steps
    
    return (x,y)



