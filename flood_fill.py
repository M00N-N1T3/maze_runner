"""
Progress 
"""
from math import modf
from world import world
import mechanics
import movement_logics

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


def hunt_north(current_cell: int|float , cells_ref: list,paths_dict: dict, visited_list: list,occupied_cells: list, target: list|tuple, target_column: list, target_row: list):
    
    
    if current_cell in target_column:
        if 'up' in paths_dict.keys() and paths_dict['up'] != None and cells_ref[int(paths_dict['up'])] not in occupied_cells:
            current_cell = paths_dict['up']
            visited_list.append(cells_ref[current_cell])
            return True, current_cell
        
    if current_cell in target_row:
        if current_cell < cells_ref.index(target):
            
            if 'right' in paths_dict.keys() and paths_dict['right'] != None and cells_ref[int(paths_dict['right'])] not in occupied_cells:
                current_cell = paths_dict['right']
                visited_list.append(cells_ref[current_cell])
                return True, current_cell
            
            if 'left' in paths_dict.keys() and paths_dict['left'] != None and cells_ref[int(paths_dict['left'])] not in occupied_cells:
                current_cell = paths_dict['left']
                visited_list.append(cells_ref[current_cell])
                return True, current_cell
        else:
            
            if 'left' in paths_dict.keys() and paths_dict['left'] != None and cells_ref[int(paths_dict['left'])] not in occupied_cells:
                current_cell = paths_dict['left']
                visited_list.append(cells_ref[current_cell])
                return True, current_cell
            
            if 'right' in paths_dict.keys() and paths_dict['right'] != None and cells_ref[int(paths_dict['right'])] not in occupied_cells:
                current_cell = paths_dict['right']
                visited_list.append(cells_ref[current_cell])
                return True, current_cell

    
    
    if 'up' in paths_dict.keys() and paths_dict['up'] != None and cells_ref[int(paths_dict['up'])] not in occupied_cells:
        current_cell = paths_dict['up']
        visited_list.append(cells_ref[current_cell])
        return True, current_cell
    
    if current_cell < cells_ref.index(target):
    
        if 'right' in paths_dict.keys() and paths_dict['right'] != None and cells_ref[int(paths_dict['right'])] not in occupied_cells:
            current_cell = paths_dict['right']
            visited_list.append(cells_ref[current_cell])
            return True, current_cell
        
        if 'left' in paths_dict.keys() and paths_dict['left'] != None and cells_ref[int(paths_dict['left'])] not in occupied_cells:
            current_cell = paths_dict['left']
            visited_list.append(cells_ref[current_cell])
            return  True, current_cell 
    else:
        
        if 'left' in paths_dict.keys() and paths_dict['left'] != None and cells_ref[int(paths_dict['left'])] not in occupied_cells:
            current_cell = paths_dict['left']
            visited_list.append(cells_ref[current_cell])
            return True, current_cell
        
        if 'right' in paths_dict.keys() and paths_dict['right'] != None and cells_ref[int(paths_dict['right'])] not in occupied_cells:
            current_cell = paths_dict['right']
            visited_list.append(cells_ref[current_cell])
            return True, current_cell
        

    if 'down' in paths_dict.keys() and paths_dict['down'] != None and cells_ref[int(paths_dict['down'])] not in occupied_cells:
        current_cell = paths_dict['down']
        visited_list.append(cells_ref[current_cell])
        return True, current_cell
    
    # if len(paths_dict) == 1 and cells_ref[int(paths_dict['up'])] not in occupied_cells:
    #     current_cell = paths_dict[key]
    #     visited.append(cells_ref[current_cell])
    return False, current_cell
    

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
    # rows = [[column[j] for column in columns] for j in range(len(columns[0]))]
    
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


def target_distance(columns_ref: list|tuple, rows_ref: list|tuple, exit_column_index: int, current_cell_row_index: int, exit_cell_index: int, current_cell: int):
    """
    Determines the horizontal and vertical distance from the current cell to the target (exit) 

    Args:
        columns_ref (list | tuple): a list | tuple containing all the columns and their respective cell values
        rows_ref (list | tuple): a list | tuple containing all the rows and their respective cell values
        exit_column_index (int): the index of the column that our exit is in 
        current_cell_row_index (int): the index of the row that our current cell is in
        exit_cell_index (int): the index_value of the exit in the maze grid as a whole
        current_cell_index (int): the index of the current cell that we on 

    Returns:
        int : The horizontal distance from the current cell to the column of the target (exit)
        int : The vertical distance from the current cell to the row of the target (exit)
    """
    
    
    # # we have rows that contains how many rows we have in our grid
    # distance_row = rows_ref[cc_row_index] # the row that I am in and its values
    # tmp = end_point_column_index    # the column that our target is in 
    
    # the current row of the cell and all the values in that row
    for index_value in rows_ref[current_cell_row_index]: 
        
        # if the said value (index_value) is in both our column and row, that 
        # makes it the linkage point between the column and row
        if index_value in columns_ref[exit_column_index]:
             
            # the denominator is the common value in both lists
            denominator = index_value
            break
        
    exit_point_column = columns_ref[exit_column_index]
    # this section determines the vertical distance (up and bottom)
    if denominator > exit_cell_index:
        # the start index, is the index of the exit_cell_value in our columns list
        start = exit_point_column.index(exit_cell_index)
        # the stop index, is the index of the denominator in our columns list
        stop = exit_point_column.index(denominator)
        vertical_distance = len(exit_point_column[start:stop])
    else:
        start = exit_point_column.index(exit_cell_index)
        stop = exit_point_column.index(denominator)
        vertical_distance = len(exit_point_column[stop:start]) # counting in reverse
    
    
    # this determines the horizontal distance
    exit_point_rows = rows_ref[current_cell_row_index]
    if denominator < current_cell:
        start = exit_point_rows.index(denominator)
        stop = exit_point_rows.index(current_cell)
        horizontal_distance = len(rows_ref[start:stop])
    else:
        start = exit_point_rows.index(denominator)
        stop = exit_point_rows.index(current_cell)
        horizontal_distance = len(rows_ref[stop:start])
        
    
    return horizontal_distance, vertical_distance


def path_finder(paths,cells_ref,visited_cells,obstacle_ref,columns_ref,rows_ref,index_of_exit_column,index_of_exit_row,current_cell):


    moved = False
    for key, values in paths.items():
        
        occupied_cells = list()
        occupied_cells.extend(visited_cells)
        occupied_cells.extend(obstacle_ref)

        
        # from flood_fill import current_cell_position
        # getting the column and the row of the current cell in tour grid 
        cc_column_index, cc_row_index = current_cell_position(columns_ref,rows_ref, current_cell)
        
                                            

            


                
        # from flood_fill import target_distance
        
        # down_dis , lat_dis = target_distance(columns_ref,rows_ref,index_of_exit_column,cc_row_index,index_of_exit_point,current_cell)
            

        horizontal_priority = None
        vertical_priority = None

        
        # from flood_fill import set_priorities
        
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


def draw_obstacle(cell: list|tuple,turtle_variable, color1: str = None,color2: str = None):
    """
    Fills in the color of the obstacles/path

    Args:
        cell (list | tuple): A list of all the cell coordinates
        color (list_): The color you want to paint the cells
    """
    # starting coordinates for the cell color fill
    import turtle
    unit = 1.5
    gui_loader = ['turtle']
    # if 'turtle' in sys.argv:
    if 'turtle' in gui_loader:
        x1,y1 = cell[0]

        turtle.tracer(0)
        # turtle_variable.hideturtle()
        turtle_variable.penup()
        turtle_variable.goto(int(x1) * unit,int(y1) * unit)
        turtle_variable.pen(pendown=True,fillcolor=color1,pensize=0,pencolor=color2,speed=0)
        turtle_variable.begin_fill()
        for cord in cell:
            x,y = cord
            turtle_variable.goto(int(x) * unit,int(y) * unit)
        turtle_variable.goto(int(x1) * unit,int(y1) * unit)
        turtle_variable.end_fill()

        turtle.tracer(1)
    else:
        pass
    
    return None



def maze_runner(cells_ref,exit_points, obstacle_ref,current_cell,visited_cells,height,width,cells_size,hunt,turtle_variable,x,y,degree):
    
    # exit_point
    for key,value in exit_points.items():
        if hunt == key:
            exit = value
            break
    
    paths_available = [cell for cell in cells_ref if cell not in obstacle_ref]
    x,y = find_cell(paths_available,x,y,cells_size)

    stack, visit ,path_taken= [],visited_cells,[]

    factor = height / cells_size

    columns, rows = rows_and_columns(cells_ref,factor)
    end_point_column_index = exit_columns(columns,[exit])[0]
    end_point_row_index = exit_rows(rows,[exit])[0]

    # init
    moved = True


    # while True:
    #     # handles moving and popping from stack
    #     if moved == True:
    #         draw_obstacle(cells_ref[current_cell],turtle_variable,'Brown')
    #         path_taken.append(cells_ref[current_cell])
    #         if cells_ref[current_cell] == cells_ref[exit]:
    #             # print("Winner")
    #             break
    #         moved = False
    #     else:
    #         rev_path_taken = list(reversed(path_taken))
    #         current_cell = stack.pop()

    #         for path in rev_path_taken:
    #             if cells_ref[current_cell] == path:
    #                 break
    #             draw_obstacle(path,turtle_variable,'White')
    #             del path_taken[path_taken.index(path)]


    #     nb, dic, factor = neighboring_cell(height,width,cells_size,current_cell)


    #     stack_it , paths = stack_control(cells_ref,dic,visit,obstacle_ref)
    #     if stack_it:
    #         stack.append(int(current_cell))

    #     current_cell , moved = path_finder(paths,cells_ref,visit,obstacle_ref,columns,rows,end_point_column_index,end_point_row_index,current_cell)


    while True:

        for i in range(30):
            # handles moving and popping from stack
            if moved == True:
                draw_obstacle(cells_ref[current_cell],turtle_variable,'Brown')
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
                    draw_obstacle(path,turtle_variable,'White')
                    del path_taken[path_taken.index(path)]


            nb, dic, factor = neighboring_cell(height,width,cells_size,current_cell)


            stack_it , paths = stack_control(cells_ref,dic,visit,obstacle_ref)
            if stack_it:
                stack.append(int(current_cell))

            current_cell , moved = path_finder(paths,cells_ref,visit,obstacle_ref,columns,rows,end_point_column_index,end_point_row_index,current_cell)
        break
    return path_taken



def find_cell(cell_ref,pos_x,pos_y,cell_size):

    for cell in cell_ref:
        cords = cell[0]
        if pos_x in range(cords[0],cords[0]+cell_size) and pos_y in range(cords[1],cords[1]+cell_size):
            cords_x = cords[0]+2
            cords_y = cords[1]+2
            
            return cords_x, cords_y

    return 0,0

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
    turns = 0
    while True:

        if actual_degree == current_degree:
            return 0

        if current_degree < 0:
            if current_degree < actual_degree:
                current_degree = current_degree + 90
                turns += 1  # turn right
            else:
                current_degree = current_degree - 90
                turns-= 1   # turn left
        else:
            if current_degree < actual_degree:
                current_degree = current_degree + 90
                turns -= 1  # turn left
            else:
                current_degree = current_degree - 90
                turns+= 1   # turn right

        if current_degree == actual_degree:
            break

    return turns


def generate_commands(cords,turtle_variable,path_taken,cell_ref,factor, cell_size = 4):
    indexes, commands, old,breaker = [], [], None,None
    x,y,current_degree = cords
    
    for cell in path_taken:
        
        if cell in cell_ref:
            indexes.append(cell_ref.index(cell))

    b = 0
    for path in indexes:

        # using degrees we can then decide if we should turn or not
        if old != path and old != None:
            if old + 1 ==  path:
                actual_degree = 90
                turns = rotate_robot(actual_degree,current_degree)
                for i in range(abs(turns)):
                    if turns == 0:
                        break
                    elif turns > 0:
                        commands.append('Right')
                    else:
                        commands.append('Left')
                com = " ".join(['Forward',f'{cell_size}'])
                commands.append(com)

            elif old - 1 == path:
                actual_degree = 270
                turns = rotate_robot(actual_degree,current_degree)
                for i in range(abs(turns)):
                    if turns == 0:
                        break
                    elif turns > 0:
                        commands.append('Right')
                    else:
                        commands.append('Left')
                com = " ".join(['Forward',f'{cell_size}'])
                commands.append(com)

            elif old - factor == path:
                actual_degree = 180
                turns = rotate_robot(actual_degree,current_degree)
                for i in range(abs(turns)):
                    if turns == 0:
                        break
                    elif turns > 0:
                        commands.append('Right')
                    else:
                        commands.append('Left')
                com = " ".join(['Forward',f'{cell_size}'])
                commands.append(com)

            elif old + factor == path:
                actual_degree = 0
                turns = rotate_robot(actual_degree,current_degree)
                for i in range(abs(turns)):
                    if turns == 0:
                        break
                    elif turns > 0:
                        commands.append('Right')
                    else:
                        commands.append('Left')
                com = " ".join(['Forward',f'{cell_size}'])
                commands.append(com)

            current_degree = actual_degree
            old = path
        else:
            com = " ".join(['Forward',f'{cell_size}'])
            old = path

    return commands
