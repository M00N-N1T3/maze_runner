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
    
    
    
def og():
#             for key, values in paths.items():
                
#             occupied_cells = list()
#             occupied_cells.extend(visit)
#             occupied_cells.extend(obs)
               
               
#             if hunt == 'north':
            
#                 if cc in end_column:
#                     # if 'up' in paths.keys() and paths['up'] != None and cells[int(paths['up'])] not in visit and  cells[int(paths['up'])] not in obs:
#                     if 'up' in paths.keys() and paths['up'] != None and cells[int(paths['up'])] not in occupied_cells:
#                         cc = paths['up']
#                         visit.append(cells[cc])
#                         break
                    
#                 if cc in end_row:
#                     if cc < cells.index(end):
                        
#                         if 'right' in paths.keys() and paths['right'] != None and cells[int(paths['right'])] not in occupied_cells:
#                             cc = paths['right']
#                             visit.append(cells[cc])
#                             break
                        
#                         if 'left' in paths.keys() and paths['left'] != None and cells[int(paths['left'])] not in occupied_cells:
#                             cc = paths['left']
#                             visit.append(cells[cc])
#                             break  
#                     else:
                        
#                         if 'left' in paths.keys() and paths['left'] != None and cells[int(paths['left'])] not in occupied_cells:
#                             cc = paths['left']
#                             visit.append(cells[cc])
#                             break
                        
#                         if 'right' in paths.keys() and paths['right'] != None and cells[int(paths['right'])] not in occupied_cells:
#                             cc = paths['right']
#                             visit.append(cells[cc])
#                             break
            

                
                
#                 if 'up' in paths.keys() and paths['up'] != None and cells[int(paths['up'])] not in occupied_cells:
#                     cc = paths['up']
#                     visit.append(cells[cc])
#                     break
                
#                 if cc < cells.index(end):
                
#                     if 'right' in paths.keys() and paths['right'] != None and cells[int(paths['right'])] not in occupied_cells:
#                         cc = paths['right']
#                         visit.append(cells[cc])
#                         break
                    
#                     if 'left' in paths.keys() and paths['left'] != None and cells[int(paths['left'])] not in occupied_cells:
#                         cc = paths['left']
#                         visit.append(cells[cc])
#                         break  
#                 else:
                    
#                     if 'left' in paths.keys() and paths['left'] != None and cells[int(paths['left'])] not in occupied_cells:
#                         cc = paths['left']
#                         visit.append(cells[cc])
#                         break
                    
#                     if 'right' in paths.keys() and paths['right'] != None and cells[int(paths['right'])] not in occupied_cells:
#                         cc = paths['right']
#                         visit.append(cells[cc])
#                         break
                    

#                 if 'down' in paths.keys() and paths['down'] != None and cells[int(paths['down'])] not in occupied_cells:
#                     cc = paths['down']
#                     visit.append(cells[cc])
#                     break
                
#                 if len(paths) == 1 and cells[int(paths['up'])] not in occupied_cells:
#                     cc = paths[key]
#                     visit.append(cells[cc])
#                     break
    pass