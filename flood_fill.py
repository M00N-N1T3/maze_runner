"""
Progress 
"""


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
    
    tmp = []
    for exit in exits:
        exit_column_index = [column  for column in columns_ref if exit in column][0]
        tmp.append(columns_ref.index(exit_column_index))
        
    return tmp

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
    
     
    tmp1 = []
    for exit in exits:
        exit_row_index = [row for row in rows_ref if exit in row][0]
        tmp1.append(rows_ref.index(exit_row_index))
        
    return tmp1
    
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


def path_finder(paths,visited_cells,obstacle_ref,columns_ref,rows_ref,index_of_exit_column,index_of_exit_row,index_of_exit_point,current_cell):

    for key, values in paths.items():
        
        occupied_cells = list()
        occupied_cells.extend(visited_cells)
        occupied_cells.extend(obstacle_ref)

        
        # from flood_fill import current_cell_position
        # getting the column and the row of the current cell in tour grid 
        cc_column_index, cc_row_index = current_cell_position(columns_ref,rows_ref, current_cell)
        
                                            

            


                
        # from flood_fill import target_distance
        
        down_dis , lat_dis = target_distance(columns_ref,rows_ref,index_of_exit_column,cc_row_index,index_of_exit_point,current_cell)
            

        horizontal_priority = None
        vertical_priority = None
        
        
        # from flood_fill import set_priorities
        
        horizontal_priority, vertical_priority, horizontal_secondary,vertical_secondary = set_priorities(cc_column_index,cc_row_index,index_of_exit_column,index_of_exit_row)
                    

        if horizontal_priority in paths.keys() and paths[horizontal_priority] != None and obstacle_ref[int(paths[horizontal_priority])] not in occupied_cells:
            cc = paths[horizontal_priority]
            visited_cells.append(obstacle_ref[cc])
            moved = True
            break 
        elif vertical_priority in paths.keys() and paths[vertical_priority] != None and obstacle_ref[int(paths[vertical_priority])] not in occupied_cells:
            cc = paths[vertical_priority]
            visited_cells.append(obstacle_ref[cc])
            moved = True
            break                         
        elif horizontal_secondary in paths.keys() and paths[horizontal_secondary] != None and obstacle_ref[int(paths[horizontal_secondary])] not in occupied_cells:
            cc = paths[horizontal_secondary]
            visited_cells.append(obstacle_ref[cc])
            moved = True
            break 
        elif vertical_secondary in paths.keys() and paths[vertical_secondary] != None and obstacle_ref[int(paths[vertical_secondary])] not in occupied_cells:
            cc = paths[vertical_secondary]
            visited_cells.append(obstacle_ref[cc])
            moved = True
            break
        else:
            cc = current_cell
            moved = False
            
        return cc, moved