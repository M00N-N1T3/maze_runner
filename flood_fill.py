"""
Progress 
"""


def stack_control(cells_ref: list|tuple , neighbors_dict: dict, visited_cells: list,obstacles: list):
    # registering our surrounding (r= 0, l= 1, up=2 , down=3)
    num_of_paths = 0
    

    tmp = dict()
    for key, value in neighbors_dict.items():    # stack control
        key_value = neighbors_dict[key] 

        if key_value!= None:
        
            # if cells_ref[int(key_value)] in obstacles:
            #     # we will ignore it if it is a wall
            continue
            
            # elif cells_ref[int(key_value)] not in visited_cells and cells_ref[int(key_value)] not in obstacles:
        if cells_ref[int(key_value)] not in visited_cells and cells_ref[int(key_value)] not in obstacles:
            tmp[key]= int(key_value)
            num_of_paths += 1
            
            # if this cell has more than one path, we add it to stack right
            if num_of_paths > 1:
                return True
                
    
    return False