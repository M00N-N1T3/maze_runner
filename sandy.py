# path finder

from math import modf
from test_base import captured_io
from io import StringIO
from sands import robot_start, main_logic
import turtle
from sandbox import generate_maze, cell_design

# turtle knows nothing in the start of the game
# Then it travels and as it travels towards the target 

# When traveling it marks its surrounding 
# marking walls and and paths
# adding routes with multiple intersections and adding it into stack 
# We always tryna move towards the target 

# If reach a dead end, we pop out of stack...
# TO speed up this we would need to only add intersections to stack
# An intersection will be classified as a cell having two or more neighbors 



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





def draw_obstacle(cell: list|tuple, color: str):
    """
    Fills in the color of the obstacles/path

    Args:
        cell (list | tuple): A list of all the cell coordinates
        color (list_): The color you want to paint the cells
    """
    # starting coordinates for the cell color fill
    
    if color == 'black':
        turtle.pencolor('white')
    else:
        turtle.pencolor('black')
        
        
    x1,y1 = cell[0]

    # turtle.tracer(0)
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(int(x1),int(y1))
    turtle.pen(pendown=True,fillcolor=color,pensize=0,speed=0)
    turtle.begin_fill()
    for cord in cell:
        x,y = cord
        turtle.goto(int(x),int(y))
    turtle.goto(int(x1),int(y1))
    turtle.end_fill()

    # turtle.tracer(1)
    return




if __name__ == '__main__':
    
    # hunt = 'north'
    hunt = 'south'
    h, w, cs = int(200*1.5), int(100*1.5), int(50)
    turtle.getscreen()
    
    cells = generate_maze(h,w,cs)
    obs= []
    
    f = h / cs *2
    # list columns 
    # columns, tmp = [], []

    # for cell in cells:
    #     tmp.append(cells.index(cell))
    #     if len(tmp) == f:
    #         columns.append(tmp)
    #         tmp=[]
        
    # number of rows in a
    # rows = [[column[j] for column in columns] for j in range(len(columns[0]))]
    
    
    from flood_fill import rows_and_columns
    
    columns, rows = rows_and_columns(cells,f)
    
    
    
    
    for cell in cells:
        draw_obstacle(cell,'White')
    
    
            
    test, stack, visit ,path_taken= [],[],[],[]
    for cell in cells:
        if cell in obs:
            test.append(cell)
            
    if len(test) == len(obs):
        print('success')
        
    cc  = 60
    path_taken.append(cells[cc])
    visit.append(cells[cc])

    moved = False
    # e=11
    # e=65
    e=5
    draw_obstacle(cells[e],'pink')
    end = cells[e]
    # draw_obstacle(cells[71],'pink')
    # end = cells[71]
    
    end_point_index = cells.index(end)

    from flood_fill import exit_columns, exit_rows
    

    end_point_column_index = exit_columns(columns,[end_point_index])[0]
    end_point_row_index = exit_rows(rows,[end_point_index])[0]
    
    moved = True   
    blocked = False
    
    
    # creating obs
    for i in range(0, len(cells)-1,7):
        if i in [0, 12, 24, 36, 48, 60] :#rows(end_point_row_index):
            continue
        if i == 11:
            continue
        if i == 35:
            continue
        # if i == 12:
        #     continue
        # if i == 24:
            continue
        if i != 0:
            draw_obstacle(cells[i],'green')
            obs.append(cells[i])
            
    for i in range(12, 25):
        
        if i == 15 :
            continue
        if i in [11,23,35,47,59,24]:
            continue

        
        if i != 0:
            draw_obstacle(cells[i],'green')
            obs.append(cells[i])
        
    moved = True
    while True:
    # for i in range(0,30):
        
        
        if moved == True:
            draw_obstacle(cells[cc],'brown')
            path_taken.append(cells[cc])
            if cells[cc] == end:
                print("Winner")
                break
            moved = False
        else:
            path_taken = list(reversed(path_taken))
            cc = stack.pop()
            
            for path in path_taken:
                
                if cells[cc] == path:
                    break
                draw_obstacle(path,'white')
            path_taken = list(reversed(path_taken))
                
        nb, dic = neighboring_cell(h*2,w*2,cs,cc)


        from flood_fill import stack_control
        stack_it , paths = stack_control(cells,dic,visit,obs)
        if stack_it:
            stack.append(int(cc))

        
 
        for key, values in paths.items():
            
            occupied_cells = list()
            occupied_cells.extend(visit)
            occupied_cells.extend(obs)

            
            from flood_fill import current_cell_position
            cc_column_index, cc_row_index = current_cell_position(columns,rows, cc)
            
                                                

               
            if hunt == 'south': 

                        
                from flood_fill import target_distance
                
                down_dis , lat_dis = target_distance(columns,rows,end_point_column_index,cc_row_index,end_point_index,cc)
                    

                horizontal_priority = None
                vertical_priority = None
                
                
                from flood_fill import set_priorities
                
                horizontal_priority, vertical_priority, horizontal_secondary,vertical_secondary = set_priorities(cc_column_index,cc_row_index,end_point_column_index,end_point_row_index)
                          

                if horizontal_priority in paths.keys() and paths[horizontal_priority] != None and cells[int(paths[horizontal_priority])] not in occupied_cells:
                    cc = paths[horizontal_priority]
                    visit.append(cells[cc])
                    moved = True
                    break 
                elif vertical_priority in paths.keys() and paths[vertical_priority] != None and cells[int(paths[vertical_priority])] not in occupied_cells:
                    cc = paths[vertical_priority]
                    visit.append(cells[cc])
                    moved = True
                    break                         
                elif horizontal_secondary in paths.keys() and paths[horizontal_secondary] != None and cells[int(paths[horizontal_secondary])] not in occupied_cells:
                    cc = paths[horizontal_secondary]
                    visit.append(cells[cc])
                    moved = True
                    break 
                elif vertical_secondary in paths.keys() and paths[vertical_secondary] != None and cells[int(paths[vertical_secondary])] not in occupied_cells:
                    cc = paths[vertical_secondary]
                    visit.append(cells[cc])
                    moved = True
                    break
                                            
                    
                    
                

 
                # if len(paths) ==0:
                #     cc = stack.pop(0)
                #     moved = True
                #     break 
            elif hunt == 'north':
                from flood_fill import hunt_north
                works, new_cc =  hunt_north(cc,cells,paths,visit,occupied_cells,end,end_point_column_index,end_point_row_index)
                


     
                    


        
    print('Execution done')
    turtle.mainloop()