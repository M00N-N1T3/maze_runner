"""
This is the main maze solver module. I tried to very much implement theories and elements found in
the flood fill algorithm. The attempt came out with little success but I was able to create and
produce something similar to flood fill, but with  a dfs(depth first approach). 
"""
from math import modf
from world import world
import movement_logics


# unit = 1.5
unit = 1

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


    return now, sides, factor

def stack_control(cells_ref: list|tuple , neighbors_dict: dict, visited_cells: list,obstacles: list):
    """
    Designed to control the flow of the stack. Based off the neighbors it 
    receives it determines whether the current index we are on should be saved onto stack
    

    Args:
        cells_ref (list | tuple): a list of all the cells in your maze
        neighbors_dict (dict): a dictionary of the available neighbors
        visited_cells (list): a list of all the visited cells
        obstacles (list): a list of all the available obstacles 
    Returns:
        bool: True / False. If true the current cell index we are on gets saved to stack
        dict: _description_
    """
    num_of_paths = 0
    

    tmp = dict()
    for key, value in neighbors_dict.items():    # stack control
        key_value = neighbors_dict[key] 

        if key_value == None:
            continue
            
        if cells_ref[int(key_value)] not in visited_cells and cells_ref[int(key_value)] not in obstacles:
            tmp[key]= int(key_value)
            num_of_paths += 1
            
            # if this cell has more than one path, we add it to the stack
            if num_of_paths > 1:
                return True, tmp
                
    
    return False, tmp


def rows_and_columns(cells_ref: list|tuple, factor: int):
    """
    Determines the number of rows and columns within your maze gride.
    Then splits it into separate list (rows and columns)
    
    The columns list contains nested lists, and each list contains cell indexes relevant to that column
    The rows list also contains nested list, and each row list contains cell indexes relevant to that row

    Args:
        cells_ref (list | tuple): _description_
        factor (int): _description_

    Returns:
        list : a list containing all the columns and its indexes 
        list : a lits containing all the rows and its indexes
    """
    
    
    columns, tmp = [], []

    for cell in cells_ref:
        tmp.append(cells_ref.index(cell))
        if len(tmp) == factor:
            columns.append(tmp)
            tmp=[]
    
    
    
    rows = []
    
    for i in range(len(columns[0])):
        tmp = []
        for column in columns:
            tmp.append(column[i])
        rows.append(tmp)
    
    return columns, rows


def exit_columns(columns_ref: list|tuple, exits: list):
    """
    Returns the relevant columns that contains the maze exits

    Args:
        columns_ref (list | tuple): a list of of all the columns in the maze grid
        cell_ref (list | tuple): a list of all the available cells in the maze grid
        exits (list): a list of all th available exits
    Returns:
        list : a list of the column indexes that contains the exits points of the maze
    """

        
    for exit in exits:
        for column in columns_ref:
            if exit in column:
                exit_col = column
                break
    
    # get the  index of the col
    return exit_col

def exit_rows(rows_ref: list|tuple, exits: list):
    """
    Returns the relevant rows that contains the maze exits

    Args:
        rows_ref (list | tuple): a list of of all the rows in the maze grid
        cell_ref (list | tuple): a list of all the available cells in the maze grid
        exits (list): a list of all th available exits
    Returns:
        list : a list of the rows indexes that contains the exits points of the maze
    """
    
    
    for exit in exits:
        for row in rows_ref:
            if exit in row:
                exit_row = row
                break
    return row
    
    
def current_cell_position(columns_ref: list|tuple, rows_ref: list|tuple, current_cell_index):
    """
    Using the index of the current_cell (cc), the cell we currently on,
    we will return the column index of that cell. The column index is 
    the column number that the 
    

    Args:
        columns_ref (list | tuple): a list | tuple containing all the columns and their respective cell values
        rows_ref (list | tuple): a list | tuple containing all the rows and their respective cell values
        current_cell_index (int): the index of the current cell that we on 

    Returns:
        int : The index value of the column that our cell is in 
        int : The index value of the 
    """
    
    for column in columns_ref:
        
        if current_cell_index in column:
            # cc = current_cell, we returning the index number of
            column_index_of_cc = columns_ref.index(column)
            break
        
    for row in rows_ref:
        
        if current_cell_index in row:
            row_index_of_cc = rows_ref.index(row)
            break
    
    return column_index_of_cc, row_index_of_cc


def set_priorities(cc_column_index: int,cc_row_index, exit_point_column_index: int, exit_point_rows_index: int ):
    
    if cc_column_index > exit_point_column_index:
        vertical_priority = 'left'
        vertical_secondary = 'right'
    else:
        vertical_priority = 'right'
        vertical_secondary = 'left'   

    if cc_row_index > exit_point_rows_index:
        horizontal_priority = 'down'
        horizontal_secondary = 'up'
    else:
        horizontal_priority = 'up'
        horizontal_secondary = 'down'

    
    return horizontal_priority,vertical_priority,horizontal_secondary,vertical_secondary


def path_finder(paths,cells_ref,visited_cells,obstacle_ref,columns_ref,rows_ref,index_of_exit_column,index_of_exit_row,current_cell):
    """
    Using list index referencing, we are able to track and trace which path to take
    when trying to solve the maze.

    Args:
        paths (dict): a dictionary containing all the relevant neighbors to our current cell
        cells_ref (list): a list of all the cells in our grid
        visited_cells (list): a list of all the cells we have previously visited/checked
        obstacle_ref (list): a list of all the available obstacles in our maze grid
        columns_ref (list): a list of all the columns in the grid and its respective cell indexes (all the indexes of the cells in a particular column)
        rows_ref (list): a list of all the rows in the grid and its respective cell indexes
        index_of_exit_column (int): the index of the column that contains the exit to the maze
        index_of_exit_row (int): the index of the row that contains the exit to the maze
        current_cell (int): the current cell(index) that we currently standing on

    Returns:
        int : current_cell - the new cell we should move to
        bool: moved - a bool value that confirms whether we moved or not 
    """

    moved = False
    for key, values in paths.items():
        
        occupied_cells = list()
        occupied_cells.extend(visited_cells)
        occupied_cells.extend(obstacle_ref)


        # getting the column and the row of the current cell in tour grid
        cc_column_index, cc_row_index = current_cell_position(columns_ref,rows_ref, current_cell)


        horizontal_priority = None
        vertical_priority = None

        horizontal_priority, vertical_priority, horizontal_secondary,vertical_secondary = set_priorities(cc_column_index,cc_row_index,index_of_exit_column,index_of_exit_row)


        if horizontal_priority in paths.keys() and paths[horizontal_priority] != None and cells_ref[int(paths[horizontal_priority])] not in occupied_cells:
            current_cell = paths[horizontal_priority]
            visited_cells.append(cells_ref[current_cell])
            moved = True

            break 
        elif vertical_priority in paths.keys() and paths[vertical_priority] != None and cells_ref[int(paths[vertical_priority])] not in occupied_cells:
            current_cell = paths[vertical_priority]
            visited_cells.append(cells_ref[current_cell])
            moved = True

            break
        elif horizontal_secondary in paths.keys() and paths[horizontal_secondary] != None and cells_ref[int(paths[horizontal_secondary])] not in occupied_cells:
            current_cell = paths[horizontal_secondary]
            visited_cells.append(cells_ref[current_cell])
            moved = True

            break 
        elif vertical_secondary in paths.keys() and paths[vertical_secondary] != None and cells_ref[int(paths[vertical_secondary])] not in occupied_cells:
            current_cell = paths[vertical_secondary]
            visited_cells.append(cells_ref[current_cell])
            moved = True

            break

            
    return current_cell,moved


# def draw_obstacle(cell: list|tuple,turtle_variable, color1: str = None,color2: str = None):
    # """
    # Fills in the color of the obstacles/path

    # Args:
    #     cell (list | tuple): A list of all the cell coordinates
    #     color (list_): The color you want to paint the cells
    # """
    # # starting coordinates for the cell color fill
    # import turtle

    # if 'turtle' in gui_loader:
    #     x1,y1 = cell[0]

    #     turtle.tracer(0)
    #     turtle_variable.hideturtle()
    #     turtle_variable.penup()
    #     turtle_variable.goto(int(x1),int(y1))
    #     # turtle_variable.goto(int(x1) * unit,int(y1) * unit)
    #     turtle_variable.pen(pendown=True,fillcolor=color1,pensize=0,pencolor=color2,speed=0)
    #     turtle_variable.begin_fill()
    #     for cord in cell:
    #         x,y = cord
    #         turtle_variable.goto(int(x) ,int(y))
    #         # turtle_variable.goto(int(x) * unit,int(y) * unit)
    #     turtle_variable.goto(int(x1),int(y1))
    #     # turtle_variable.goto(int(x1) * unit,int(y1) * unit)
    #     turtle_variable.end_fill()

    #     # turtle.tracer(1)
    # else:
    #     pass
    
    # return None



def maze_run(cells_ref,exit_points, obstacle_ref,current_cell,visited_cells,height,width,cells_size,hunt,turtle_variable,x,y,degree):
    """
    The main maze run function. This function solves the maze via a process similar to depth first search. 
    Using cell referencing we are able to draw a path from the robots current position all the way to the exit.

    Args:
        cells_ref (list): a list of all the cells in our grid
        exit_points (list): a list containing all the indexes of the exit cells in our grid
        obstacle_ref (list): a list of all the available obstacles in our maze grid
        current_cell (int): the current cell(index) that we currently standing on
        visited_cells (list): a list of all the cells we have previously visited/checked
        height (int): the height of the maze (maze_grid)
        width (int): the width of the maze (maze_grid)
        cells_size (int): teh size of each cell in our grid
        hunt (str): the direction through which we want to exit the maze ( e.g top, we would look for an exit on the top edge of teh maze)
        turtle_variable (object): the turtle / robot we want to solve the maze with (used only during gui)
        x (int): the current x coordinate of the robot in the maze
        y (int): the current y coordinate of the robot in the maze
        degree (int): teh current degree of orientation of the robot (where the robot is facing)

    Returns:
        list : the path that must be taken in order to solve the maze (relative to the robots current position in the maze)
    """
    # exit_point
    for key,value in exit_points.items():
        if hunt == key:
            exit = value
            break
    
    paths_available = [cell for cell in cells_ref if cell not in obstacle_ref]
    x1,y2, cc = find_cell(paths_available,x,y,cells_size)

    stack, visit ,path_taken= [],visited_cells,[]

    factor = height / cells_size

    columns, rows = rows_and_columns(cells_ref,factor)
    end_point_column_index = exit_columns(columns,[exit])[0]
    end_point_row_index = exit_rows(rows,[exit])[0]

    # init
    moved = True


    while True:
        # handles moving and popping from stack
        if moved == True:
            # draw_obstacle(cells_ref[current_cell],turtle_variable,'Brown')
            path_taken.append(cells_ref[current_cell])
            if cells_ref[current_cell] == cells_ref[exit]:
                # print("Winner")
                break
            moved = False
        else:
            rev_path_taken = list(reversed(path_taken))
            current_cell = stack.pop()

            for path in rev_path_taken:

                if cells_ref[current_cell] == path:
                    break
                
                if cells_ref[441] != path:
                    # draw_obstacle(path,turtle_variable,'White')
                    del path_taken[path_taken.index(path)]


        nb, dic, factor = neighboring_cell(height,width,cells_size,current_cell)


        stack_it , paths = stack_control(cells_ref,dic,visit,obstacle_ref)
        if stack_it:
            stack.append(int(current_cell))

        current_cell , moved = path_finder(paths,cells_ref,visit,obstacle_ref,columns,rows,end_point_column_index,end_point_row_index,current_cell)

    return path_taken



def find_cell(cell_ref,pos_x,pos_y,cell_size):
    """
    finds the current cell that contains the current x and y coordinate that the robot is at

    Args:
        cell_ref (list): a list of all the available cells in the maze grid
        pos_x (int): the current x coordinate of the robot in the maze
        pos_y (int): the current y coordinate of the robot in the maze
        cell_size (int): the size of a single cell in our grid
    """

    for cell in cell_ref:
        cords = cell[0]
        if pos_x in range(cords[0],cords[0]+cell_size) and pos_y in range(cords[1],cords[1]+cell_size):
            cords_x = cords[0]+ cell_size /2
            cords_y = cords[1]+ cell_size / 2
            
            return cords_x, cords_y,cell_ref.index(cell)
            # return cords_x* unit, cords_y * unit

    return 0,0, cell_ref.index(cell)

def world_pos_tracker(turtle_variable):
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
    # message = f" > {robot_name} now at position {tuple(position)}."
    return position,degree


def rotate_robot(actual_degree, current_degree):
    """
    Calculates the number of times to turn the robot left/right
    so that it is facing the correct direction that it needs to move forward in

    Args:
        actual_degree (int): the degree the robot needs to be facing in order to move forward in the specified direction
        current_degree (int): the degree the robot is currently facing
    Returns:
        int : the number of times the robot needs to turn and in what direction (- left / + right)
    """
    
    north = [90,-270]
    south = [-90,270]
    east = [0,360]
    west = [180,-180]

    turn = ['Right','Right']

    if current_degree in north:
        # the idea is if we by 90/-270 and we want to go to 180
        if actual_degree in north:
            return None
        
        if actual_degree in west:
            turn = ['Left']
        elif actual_degree in east:
            turn = ['Right']

    elif current_degree in south:
        
        if actual_degree in south:
            return None

        if actual_degree in east:
            turn = ['Left']
        elif actual_degree in west:
            turn = ['Right']

    elif current_degree in east:
        
        if actual_degree in east:
            return None
        
        if actual_degree in north:
            turn = ['Left']
        elif actual_degree in south:
            turn = ['Right']

    else:
        
        if actual_degree in west:
            return None
        
        if actual_degree in north:
            turn = ['Right']
        elif actual_degree in south:
            turn = ['Left']

    return turn


def command_splitter(command: str):
    """Splits the command into two parts, command and parameter

    Args:
        command (str): command given to the robot

    Returns:
        list: the list consists of the command and its parameter if any
    """

    commands = command.split(" ")
    return commands



def command_handler(robot_name,command,x,y,degree,turtle_variable,obstacle):

    # The command is split in two parts in list format [Command, Parameter]
    # in our com_n_par list, the command is always at index 0
    command = command_splitter(command)


    if "Right" in command or "Left" in command:
        x,y,degree,message,invalid_com = movement_logics.turn_logic(robot_name,command,x,y,degree,turtle_variable)
    else:
        x,y,degree,message,invalid_com = movement_logics.movement_logic(robot_name,command,x,y,degree,turtle_variable,obstacle)

    return x,y,degree,message,invalid_com

def fix_degree(current_degree):
    """
    Converts the negative degree to its corresponding positive degree
    Args:
        current_degree (int): the turtles current degree

    Returns:
        int : the corresponding positive degree
    """

    
    if current_degree == -270:
        current_degree = 90
    elif current_degree == -90:
        current_degree = 270
    elif current_degree == -180:
        current_degree = 180
    elif current_degree == 360:
        current_degree = 0

    return current_degree

def generate_steps_command(x,y,current_degree,cell_size):
    """
    Generates a command that gets fed into the command handler.
    The command handler is in charge of controlling the robots movement, thus based
    of the command that gets generated by this function, the robot shell execute what needs to be done

    Args:
        x (int): the robots current x coordinate
        y (int): the robots current y coordinate
        current_degree (int): the robots current degree of orientation
        cell_size (int): teh size of a single cell in our maze grid

    Returns:
        str : the command that the robot needs to execute
    """
    if current_degree == 0 and x + cell_size > 100:
        command = " ".join(['Forward',f'{100 - x}'])

    elif current_degree == 180 and x - cell_size < - 100:
        command = " ".join(['Forward',f'{100 + x}'])

    elif current_degree == 90 and y + cell_size > 200:
        command = " ".join(['Forward',f'{200 - y}'])

    elif current_degree == 270 and y - cell_size < - 200:
        command = " ".join(['Forward',f'{200 + y}'])

    else:
        command = " ".join(['Forward',f'{cell_size}'])

    return command


def solve_maze(cords,robot_name,turtle_variables,path_taken,cell_ref,obstacles,factor,hunt = "top" ,cell_size = 4,unit = 1.5):
    """
    Using the corresponding robot, solve maze will issue a set of commands that will enable the robot
    to traverse through the maze to the corresponding edge of the maze if specified.
    By default the robot will traverse to the top edge of the maze

    Args:
        cords (tuple): a tuple containing the x and y coordinate and the degree of the robot
        robot_name (str): the name of th robot
        turtle_variables (object): the turtle object (used to move the turtle gui)
        path_taken (list): a list containing all the indexes of the cells that we need to move to in order to solve the maze
        cell_ref (list): a list of all the cells in our maze grid
        obstacles (list): a list of all the obstacles in our maze grid
        factor (int): factor is the max number of cells we can hold in a single column (height / cell_size)
        hunt (str, optional): the edge of teh maze we wish to solve to. Defaults to "top".
        cell_size (int, optional): the size of a single cell in the maze grid. Defaults to 4.


    Returns:
        tuple: x,y,current_degree - the robots new position in the maze grid once it has finished traversing the maze
    """

    turtle_variable =turtle_variables
    path_cells, old_cell,breaker = [], None,None
    data = []
    x,y,current_degree = cords
    
    for cell in path_taken:
        
        if cell in cell_ref:
            path_cells.append(cell_ref.index(cell))

    # cell_size = int(cell_size /2 * unit)
    i = 0
    for new_cell in path_cells:
        
        # new function
        current_degree =fix_degree(int(current_degree))

        # using degrees we can then decide if we should turn or not
        if old_cell != new_cell and old_cell != None:
            if old_cell + 1 ==  new_cell:
                actual_degree = 90
                turns = rotate_robot(actual_degree,current_degree)


            elif old_cell - 1 == new_cell:
                actual_degree = 270
                turns = rotate_robot(actual_degree,current_degree)


            elif old_cell - factor == new_cell:
                actual_degree = 180
                turns = rotate_robot(actual_degree,current_degree)


            elif old_cell + factor == new_cell:
                actual_degree = 0
                turns = rotate_robot(actual_degree,current_degree)


            if turns != None:
                for command in turns:
                    x,y,current_degree, message, invalid_com = command_handler(robot_name,command,x,y,current_degree,turtle_variable,obstacles)
                    coordinates = (x,y,current_degree)
                    world.position_tracker(robot_name,coordinates,turtle_variable)


            command = generate_steps_command(x,y,current_degree,cell_size)

            x,y,current_degree, message, invalid_com = command_handler(robot_name,command,x,y,current_degree,turtle_variable,obstacles)
            coordinates = (x,y,current_degree)
            world.position_tracker(robot_name,coordinates,turtle_variable)
            
        else:

            # shifting into the centre of the starting cell
            if turtle_variable != None:
                position, current_degree = world_pos_tracker(turtle_variable)
                x,y = int(position[0]- cell_size / 2), int(position[1]+ cell_size /2)
                turtle_variable.goto(x,y)
            else:
                x,y = int(x - cell_size / 2), int(y+ cell_size /2)
                

        old_cell = new_cell

    return x,y,current_degree
