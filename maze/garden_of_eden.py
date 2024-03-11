"""
This maze algorithm was written in simple turtle language.
Designed to simply the maze generation part of TR_5 maze.


"""
__author__ = 'Johnny'
__version__ = '1.0'

# sandbox is where i code and test my logic
import turtle
import random
import sys
from math import modf

gui_loader = sys.argv
gui_loader = [word.lower() for word in gui_loader]
gui_loader.append('turtle')


unit = 1.5

# full function
def generate_obstacles(maze_height: int = 200, maze_width: int = 100, cell_size: int = 4 , color: str = 'white' ):
    """
    The main maze function, creates the maze for you

    Args:
        maze_height (int): The height of the maze
        maze_width (int): The width of the maze
        cell_size (int): The size of the maze outline lines
        color (str): The color of the obstacles in the maze
    """


    # initialization phase
    maze_height, maze_width = maze_height * 2 + cell_size * 2, maze_width * 2 + cell_size * 2 # accounting for external walls


    # Rule 1: of programming, if it works do not fix it, the /2 is what is keeping this from breaking
    cells = generate_maze(maze_height / 2,maze_width/2,cell_size)
    current_cell = random.randint(0, len(cells) -1)
    # calculating the maximum amount of cell our grid can hold
    max_cell = maze_height / cell_size * maze_width / cell_size

    # creating essentials
    stack, visited_cells, walls = [], [], []

    # creating exits and spawn spot
    center_of_maze = maze_center(cells,cell_size)
    exit_ref, exits, border_walls = maze_exits(cells,maze_height,cell_size)
    entrance_path = clearing_exit_pathway(maze_height,maze_width,cell_size,exits,border_walls)



    for wall in entrance_path:
        cell_design(cells,wall,visited_cells,stack,color,'black')

    for wall in border_walls:
        if wall not in exits:
            draw_obstacle(cells[wall],'black','black')
            walls.append(cells[wall])
            
        else:
            draw_obstacle(cells[wall],'Pink','Pink')
        visited_cells.append(cells[wall])
        stack.append(cells[wall])


    for cell in center_of_maze:
        cell_design(cells,cell,visited_cells,stack,'Pink','Pink')


    # starting maze generation sequence and initialization
    cell_design(cells,wall,visited_cells,stack)
    moved = True

    count = 0
    i = 0
    while len(visited_cells) != max_cell and count < len(visited_cells):
        
        if i != max_cell * 10:
            i+=1
        else:
            break
        if moved:
            neighbors, paths = neighboring_cell(maze_height,maze_width,cell_size,current_cell)
            moved = False

        if len(neighbors) != 0:
            neighbors_index = random.choice(neighbors)
            neighbors.pop(neighbors.index(neighbors_index))

        # checking if we have already visited any neighbors
        if cells[neighbors_index] in visited_cells and len(neighbors) == 0:#count == num_of_neighbors:
            current_cell =  stack_control(cells,stack)
            moved = True


        # moving, then painting the cell we in
        if not cells[neighbors_index] in visited_cells:

            # First we change the color of the cell then we are appending
            # it to both visited and stack list. (All done in the cell_design func)
            cell_design(cells,neighbors_index,visited_cells,stack,color,'black')

            # This section is what creates/draws our walls
            try:

                while True:
                    # The wall is made from a randomly chosen neighbor that was not visited
                    wall = random.choice(neighbors)
                    if cells[wall] in visited_cells or cells[wall] in exits:
                        neighbors.pop(neighbors.index(wall))
                    else:
                        break

                if not cells[wall] in walls:
                    cell_design(cells,wall,visited_cells,stack)
                    walls.append(cells[wall])
                    moved = True

                current_cell = neighbors_index

            except IndexError:
                current_cell = stack_control(cells,stack)
                moved = True

    # walls is a list of all our obstacles
    return walls, exit_ref, cells


def generate_maze(height: int, width: int, cell_size: int):
    """
    Generates a maze
    The maze is a grid containing cells/blocks of squares, of size n * n


    Args:
        height (int): Height of the maze
        width (int): Width of the maze
        cell_size (int): size of the cells
        
    Returns:
        list: A list of all the available cell coordinates
    """

    cells = spawn_obstacles(height,width,cell_size)


    return cells


# stack control
def stack_control(cells: list,stack: list):
    """
    Controls the flow of the stack memory(list)
    It retrieves data from stack memory, then returns
    the corresponding index of the data we retrieved from our cells list

    Args:
        cells (list): The list of available cells
        stack (_type_): The stack memory variable
    Returns:
        int : The index of the data within our cells list
    """
    if len(stack) -1 == 0:
        return 0
    

    # retrieving the data of the corresponding index that we popped
    index_popped = stack.pop()[::]  # NB stack list is reversed to makeup for LIFO

    # retrieving the corresponding data's index in the list of cells
    new_index = cells.index(index_popped)

    return new_index


# cell / wall functions
def create_obstacle(xcord: int, ycord: int, cell_size: int):
    """
    Draws a single cell unit / obstacle.
    One cell is a square of size cell_size * cell_size
    E.g if cell_size = 2, the size of the square/cell will be 2 by 2 (2h * 2w)

    Args:
        xcord (int): The corodinates of where to start drawing the cell on the x-axis
        ycord (int): The corodinates of where to start drawing the cell on the y-axis
        cell_size (int): The size of the cell
    
    Returns:
        tuple: A tuple of the coordinates of the cells edges(corners)
    """


    obstacle = list()
    

    obstacle.append((xcord + cell_size,ycord))
    obstacle.append((xcord + cell_size,ycord + cell_size))
    obstacle.append((xcord,ycord + cell_size))
    obstacle.append((xcord,ycord))

    # turtle.goto((xcord + cell_size,ycord))
    # turtle.goto((xcord + cell_size,ycord + cell_size))
    # turtle.goto((xcord,ycord + cell_size))
    # turtle.goto((xcord,ycord))


    return tuple(obstacle)


def spawn_obstacles(height: int = 210, width: int = 110,cell_size: int = 5):
    """
    Generates and fills the maze with cells of a specified cell s_size

    Args:
        height (int): The height of the maze / length of y-axis
        width (int): The width of the maze / length of x-axis
        cell_size (int): The size of the cell
        
    Returns:
        list: A list of all the coordinates of our cells

    cell_size also acts as the incrementing step for our print loop
    """
    # height,width = height / 2, width / 2
    height,width = int(height), int(width)

    obstacle_ref = []
    # width is the values on our x-axis on the cartesian plain
    for x in range(-width, width, cell_size):

        # height is the values on our x-axis on the cartesian plain
        for y in range(-height + cell_size, height + cell_size, cell_size):
            # generating a single cell at a time then adding to a list of references
            cell = create_obstacle(x ,y - cell_size,cell_size)
            obstacle_ref.append(cell)

    return obstacle_ref


def neighboring_cell(height: int,width: int,cell_size: int,current_cell_index: int):
    """
    Calculates and predicts the index(s) of neighboring cells
    to the current cell

    Args:
        height (int): Height of the maze
        width (int): Width of the maze
        cell_size (int): Size / Area of a single cell block
        current_cell_index (int): The index of the current cell we are in
    Returns:
        list: a list of the available neighbors
    """

    sides = dict()
    
    # The total number of cells in the maze
    cells_total = height / cell_size * width / cell_size
    # The max number of cells we can fit in a single y-axis column is known as our factor value
    factor = height / cell_size # The factor value is the main dictator of how the maze is designed
    # bottom/top walls float values
    wall_factor = format(modf(factor -1 / factor)[0],'.2f')
    # we get it by dividing 1 by factor, answer = n.wall_factor (7/8 = 0.125 | 125 = wall_factor)

    neighbors = []

    # controlling list index so that we do not get an index error
    if cells_total == current_cell_index: # len of a list is from 1 to max whereby list index is from 0 to max -1
        current_cell_index -=1            # therefore is the number generated is == max len of list, we deduct 1

    # calculating the index of the neighboring cell to the right of the current cell
    right_neighbor = current_cell_index + factor
    neighbors.append(right_neighbor)
    sides["right"] = right_neighbor


    # calculating the index of the neighboring cell to the left of the current cell
    left_neighbor = current_cell_index - factor
    neighbors.append(left_neighbor)
    sides["left"] = left_neighbor

    # calculating the index of the neighboring cell to the top of the current cell
    if format(modf(current_cell_index / factor)[0],'.2f') != wall_factor:
        upside_neighbor = current_cell_index + 1
        neighbors.append(upside_neighbor)
        sides['up'] = upside_neighbor
    else:
        sides['up'] = None

    # downside_neighbor = current_cell_index - 1
    # neighbors.append(downside_neighbor)
    if current_cell_index % factor != 0:
        downside_neighbor = current_cell_index - 1
        neighbors.append(downside_neighbor)
        sides['down'] = downside_neighbor
    else:
        sides['down'] = None

    # filtering out values less than zero or values greater than number of cells
    next = [int(n) for n in neighbors if n < cells_total+1 and n > -1]
    # filtering out the number n if n is == to the last index in the maze grid
    now = [int(n) for n in next if n != cells_total]
    
    for keys, value in sides.items():
        if value not in now:
            sides[keys] = None


    return now, sides

# maze functions

def draw_maze_border(height: int = 200, width: int = 100):
    """Draws the outside walls of our maze (borders)

    Args:
        height (int): The height of the maze / length of y-axis
        width (int): The width of the maze / length of x-axis
    """

    # In turtle home position is always set on (0,0)
    # dividing both the h and w by 2, so we can draw our maze around (0.0)
    # the (0,0) point is the center of our maze

    height = height / 2
    width = width / 2
    turtle.hideturtle()
    turtle.speed(10000)
    turtle.penup()
    turtle.goto(-width,height)
    # turtle.teleport(-width,height) | This will only work if you running python3 v 10.12
    turtle.pen(pensize=0,pendown=False)
    turtle.goto(width,height)
    turtle.goto(width,-height)
    turtle.goto(-width,-height)
    turtle.goto(-width,height)

    return


def maze_center(cell_ref: int, cell_size: int):
    """
    Generates the center of the maze.
    The center of the maze is our spawn spot

    Args:
        cell_ref (int): A list of all the cell coordinates in the maze
        cell_size (int): The size of a single cell
    Return:
        (list) : coordinates of the center of the maze
    """

    # coordinates
    left_half = 0,-cell_size
    right_half = 0,cell_size

    # The cell must contain the point 0,0 as one of its coordinates to be considered a center
    center_cord = [cell for cell in cell_ref if (left_half in cell or right_half in cell) and (0,0) in cell]

    # retrieving the index of the coordinates in our maze
    maze_center = [cell_ref.index(cord) for cord in center_cord]
    return maze_center


def maze_exits(cells_ref: list, maze_height: int, cell_size: int):
    """
    Generates the outside walls/barriers of our maze
    Then assigns an exit to the maze on each side of the maze

    Args:
        cells_ref (list): A list of all the cells in our maze

    Returns:
        tuple : a list of the exits and outside walls
    """

    # setting factor
    factor = int(maze_height / cell_size)
    # initialing temporary lists
    border_walls, filtering_corners, exits = [], [], []
    exit_ref = dict()

    # retrieving the indexes of the specified walls
    left_walls = [cells_ref.index(cell) for cell in cells_ref[:factor]]
    right_walls = [cells_ref.index(cell) for cell in cells_ref[-factor:]]
    top_walls = [index-1 for index in range(len(cells_ref),0,-factor)]
    bottom_walls = [index for index in range(0,len(cells_ref),factor)]

    # combining all the generated index data
    border_walls = left_walls  + top_walls + right_walls + bottom_walls

    # filtering out and removing the corner walls
    for index in border_walls:
        if index == 0 or index == factor-1:
            continue
        elif  index ==  len(cells_ref)-1 or index == len(cells_ref)-factor:
            continue
        else:
            filtering_corners.append(index)



    # generating a possible exit to our maze depending on the wall side
    left_exit = [index for index in left_walls if index in filtering_corners]
    exit_1 = random.choice(left_exit)
    exits.append(exit_1)
    exit_ref["west"] = exit_1

    right_exit = [index for index in right_walls if index in filtering_corners]
    exit_2 = random.choice(right_exit)
    exits.append(exit_2)
    exit_ref["east"] = exit_2

    top_exit = [index for index in top_walls if index in filtering_corners]
    exit_3 = random.choice(top_exit)
    exits.append(exit_3)
    exit_ref["north"] = exit_3

    bottom_exit = [index for index in bottom_walls if index in filtering_corners]
    exit_4 = random.choice(bottom_exit)
    exits.append(exit_4)
    exit_ref["south"] = exit_4


    return exit_ref, exits, border_walls


def clearing_exit_pathway(maze_height: int,maze_width: int,cell_size: int, exits_ref: list, borders_ref: list):
    """
    Generates the indexes of the cells around the exit of our maze
    Which can be used to dictate the placement of obstacles around
    the maze entrances

    Args:
        maze_height (int): The height of maze
        maze_width (int): The width of the maze
        cell_size (int): The size of a single cell/wall
        exits_ref (list): a list of exit/entrance cell's indexes
        borders_ref (list): A list of all the border cell's indexes

    Returns:
        list : A list of all the indexes of the cells around the exits
    """
    
    # essentials
    tmp,exit_entrances, entrance_path = [], [], []
    
    # generating pathway indexes
    for index in exits_ref:
        nc , paths=neighboring_cell(maze_height,maze_width,cell_size,index)
        tmp.extend(nc)
        # tmp.append(nc)
    exit_entrances = [index for index in tmp if index not in borders_ref]
    
    for index in exit_entrances:
        nc , paths =neighboring_cell(maze_height,maze_width,cell_size,index)
        entrance_path.extend(nc)
        
    entrance_path = [index for index in entrance_path if index not in exit_entrances]

    pathway_index = exit_entrances + entrance_path
    
    return pathway_index
        


# helper functions

def cell_design(cells_ref: list, ele_index: int, visited_cells: list, stack: list, wall_color = 'black',outline: str =None):
    """
    Designs the cell. Sets/changes  the color attributes
    of the specified element to a specified color

    Args:
        cell_ref (list): List of available cells
        ele_index (int): The index of the element we wish to modify
        visited_cells (list): List of previously visited/ modified cells
        stack (list): Stack memory of our maze
        wall_color (str, optional): The color you want to set the cell. Defaults to 'black'.
    """

    draw_obstacle(cells_ref[ele_index],wall_color,outline)
    visited_cells.append(cells_ref[ele_index])
    stack.append(cells_ref[ele_index])


def draw_obstacle(cell: list|tuple, color1: str,color2: str = None):
    """
    Fills in the color of the obstacles/path

    Args:
        cell (list | tuple): A list of all the cell coordinates
        color (list_): The color you want to paint the cells
    """
    # starting coordinates for the cell color fill
    
    # if 'turtle' in sys.argv:
    if 'turtle' in gui_loader:
        x1,y1 = cell[0]

        turtle.tracer(0)
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(int(x1) * unit,int(y1) * unit)
        turtle.pen(pendown=True,fillcolor=color1,pensize=0,pencolor=color2,speed=0)
        turtle.begin_fill()
        for cord in cell:
            x,y = cord
            turtle.goto(int(x) * unit,int(y) * unit)
        turtle.goto(int(x1) * unit,int(y1) * unit)
        turtle.end_fill()

        turtle.tracer(1)
    else:
        pass
    
    return None


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
    # (x1,y1) | pretend its 5 x 5   | (x2,y2)
    #         |---------------------|
    # point 4 = (x,y+4)     point 3 = (x+4,y+4)

    x1,y1= position1
    x2,y2 = position2


    # bug add command check here 
    # if back, all + must be -
    if x1 == x2:
        step = -1 if y2 < y1 else 1
        for y in range(y1,y2+step,step):
            if is_position_blocked(x1,y,obstacles):
                return True
    elif y1 == y2:
        step = -1 if x2 < x1 else 1
        for x in range(x1,x2+step,step):
            if is_position_blocked(x,y1,obstacles):
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
    #         | pretend its 5 x 5   |
    #         |---------------------|
    # point 4 = (x,y+4)     point 3 = (x+4,y+4)

    # line 1: x to x+4
    # line 2: y to y+4
    # line 3: x to x+4
    # line 2: y to y+4

    for obstacle in obstacles:
        x1,y1 = obstacle[0]
        if (x in range(x1,x1+5) and y in range(y1,y1+5)):
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




