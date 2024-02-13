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
    
    rows = [[column[j] for column in columns] for j in range(len(columns[0]))]
    
    return columns, rows


def exit_columns(columns_ref: list|tuple, cells_ref: list|tuple, exits: list):
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
        exit = cells_ref.index(exit)
        exit_column_index = [column  for column in columns_ref if exit in column][0]
        tmp.append(exit_column_index)
        
    return tmp

def exit_rows(rows_ref: list|tuple, cells_ref: list|tuple, exits: list):
    """
    Returns the relevant rows that contains the maze exits

    Args:
        rows_ref (list | tuple): a list of of all the rows in the maze grid
        cell_ref (list | tuple): a list of all the available cells in the maze grid
        exits (list): a list of all th available exits
    Returns:
        list : a list of the rows indexes that contains the exits points of the maze
    """
    
     
    tmp = []
    for exit in exits:
        exit = cells_ref.index(exit)
        exit_row_index = [row for row in rows_ref if exit in row][0]
        tmp.append(exit_row_index)
        
    return tmp
    
    
    


 
# def target_distance():
#     # we have rows that contains how many rows we have in our grid
#     distance_row = rows[cc_row_index] # the row that I am in and its values
#     tmp = end_point_column_index    # the column that our target is in 
    
#     for index_value in distance_row: 
#         # if the said value is in our column, that means its the denominator
#         if index_value in tmp: 
#             # the denominator is the common value in both lists
#             denominator = index_value
#             break
        
    
#     # this determines the distance to the bottom
#     if denominator > end_point_index:
#         start = end_point_column_index.index(end_point_index)
#         stop = end_point_column_index.index(denominator)
#         down_dis = len(end_point_column_index[start:stop])
#     else:
#         start = end_point_column_index.index(end_point_index)
#         stop = end_point_column_index.index(denominator)
#         down_dis = len(end_point_column_index[stop:start]) # counting in reverse
    
    
#     # this determines the left right distance
    
#     if denominator < cc:
#         start = distance_row.index(denominator)
#         stop = distance_row.index(cc)
#         lat_dis = len(distance_row[start:stop])
#     else:
#         start = distance_row.index(denominator)
#         stop = distance_row.index(cc)
#         lat_dis = len(distance_row[stop:start])
