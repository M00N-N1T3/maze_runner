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
    wall_factor = modf(factor -1 / factor)[0]
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
    if modf(current_cell_index / factor)[0] != wall_factor:
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

    turtle.tracer(0)
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

    turtle.tracer(1)
    return




if __name__ == '__main__':
    
    hunt = 'north'
    h, w, cs = int(200*1.5), int(100*1.5), int(50)
    turtle.getscreen()
    
    cells = generate_maze(h,w,cs)
    obs= []
    
    f = h / cs *2
    # list columns 
    columns, tmp = [], []

    for cell in cells:
        tmp.append(cells.index(cell))
        if len(tmp) == f:
            columns.append(tmp)
            tmp=[]
        
    # number of rows in a
    rows = [[column[j] for column in columns] for j in range(len(columns[0]))]
                
    
    
    
    
    for cell in cells:
        draw_obstacle(cell,'White')
    
    
            
    test, stack, visit ,path= [],[],[],[]
    for cell in cells:
        if cell in obs:
            test.append(cell)
            
    if len(test) == len(obs):
        print('success')
        
    cc  = 0
    path.append(cells[cc])
    visit.append(cells[cc])
    # ns = neighboring_cell(h*2,w*2,cs,cc)
    # ns = list(reversed(ns))
    # draw_obstacle(cells[cc],'red')
    # for n in ns:
    #     draw_obstacle(cells[n],'blue')
    
    moved = False
    
    draw_obstacle(cells[71],'pink')
    end = cells[71]
    end_index = cells.index(end)

    end_column = [column  for column in columns if end_index in column][0]
    end_row = [row for row in rows if end_index in row][0]
    
    moved = True   
    blocked = False
    
    
    # creating obs
    for i in range(0, len(cells)-1,7):
        if i in end_row:
            continue
        if i != 0:
            draw_obstacle(cells[i],'green')
            obs.append(cells[i])
            
    for i in range(12, 25):
        
        if i == 15:
            continue
        if i in end_row:
            continue

        
        if i != 0:
            draw_obstacle(cells[i],'green')
            obs.append(cells[i])
        
    for i in range(0,25):
        
        draw_obstacle(cells[cc],'brown')
        nb, dic = neighboring_cell(h*2,w*2,cs,cc)


        # registering our surrounding (r= 0, l= 1, up=2 , down=3)
        num_of_paths = 0
        

        tmp = dict()
        for key, value in dic.items():    # stack control
            n = dic[key] 

            if n != None:
            
                if cells[int(n)] in obs:
                    print(f'This is an obs: {dic[key]}')
                    # we will ignore it if it is a wall
                
                elif cells[int(n)] not in visit and cells[int(n)] not in obs:
                    print(f'This is a path: {n}')
                    tmp[key]= int(n)
                    num_of_paths += 1
                    
                    # if this cell has more than one path, we add it to stack right
                    if num_of_paths > 1:
                        stack.append(int(cc))
                        print(f'added to stack: {n}')

        
        # the column that cc is in
        
        
                
        for key, values in tmp.items():
            
            occupied_cells = list()
            occupied_cells.extend(visit)
            occupied_cells.extend(obs)
               
               
            if hunt == 'north':
            
                if cc in end_column:
                    # if 'up' in tmp.keys() and tmp['up'] != None and cells[int(tmp['up'])] not in visit and  cells[int(tmp['up'])] not in obs:
                    if 'up' in tmp.keys() and tmp['up'] != None and cells[int(tmp['up'])] not in occupied_cells:
                        cc = tmp['up']
                        visit.append(cells[cc])
                        break
                    
                if cc in end_row:
                    if cc < cells.index(end):
                        
                        if 'right' in tmp.keys() and tmp['right'] != None and cells[int(tmp['right'])] not in occupied_cells:
                            cc = tmp['right']
                            visit.append(cells[cc])
                            break
                        
                        if 'left' in tmp.keys() and tmp['left'] != None and cells[int(tmp['left'])] not in occupied_cells:
                            cc = tmp['left']
                            visit.append(cells[cc])
                            break  
                    else:
                        
                        if 'left' in tmp.keys() and tmp['left'] != None and cells[int(tmp['left'])] not in occupied_cells:
                            cc = tmp['left']
                            visit.append(cells[cc])
                            break
                        
                        if 'right' in tmp.keys() and tmp['right'] != None and cells[int(tmp['right'])] not in occupied_cells:
                            cc = tmp['right']
                            visit.append(cells[cc])
                            break
            

                
                
                if 'up' in tmp.keys() and tmp['up'] != None and cells[int(tmp['up'])] not in occupied_cells:
                    cc = tmp['up']
                    visit.append(cells[cc])
                    break
                
                if cc < cells.index(end):
                
                    if 'right' in tmp.keys() and tmp['right'] != None and cells[int(tmp['right'])] not in occupied_cells:
                        cc = tmp['right']
                        visit.append(cells[cc])
                        break
                    
                    if 'left' in tmp.keys() and tmp['left'] != None and cells[int(tmp['left'])] not in occupied_cells:
                        cc = tmp['left']
                        visit.append(cells[cc])
                        break  
                else:
                    
                    if 'left' in tmp.keys() and tmp['left'] != None and cells[int(tmp['left'])] not in occupied_cells:
                        cc = tmp['left']
                        visit.append(cells[cc])
                        break
                    
                    if 'right' in tmp.keys() and tmp['right'] != None and cells[int(tmp['right'])] not in occupied_cells:
                        cc = tmp['right']
                        visit.append(cells[cc])
                        break
                    

                if 'down' in tmp.keys() and tmp['down'] != None and cells[int(tmp['down'])] not in occupied_cells:
                    cc = tmp['down']
                    visit.append(cells[cc])
                    break
                
                if len(tmp) == 1 and cells[int(tmp['up'])] not in occupied_cells:
                    cc = tmp[key]
                    visit.append(cells[cc])
                    break
            
            if len(tmp) ==0:
                cc = stack.pop(0) 


     
                    

        #             if cells[b] not in visit and b > cells.index(end) and b != cc - 1:
        #                 cc = b
        #                 print('should move')
        #                 visit.append(cells[cc])
        #                 breaking = True
        #                 break
                    
                    
        #             # if cells[b] not in visit and cells[cc+f] in obs or  cells[cc+f] in visit:
        #             #     cc = b
        #             #     print('should move')
        #             #     visit.append(cells[cc])
        #             #     breaking = True
        #             #     break
                    
                    
                    
        #             if cells[b] not in visit and (cc + f) == b:
        #                 cc = b
        #                 print('should move')
        #                 visit.append(cells[cc])
        #                 breaking = True
        #                 break
                
        #         # the last edit was reversing the list
                
        #         # adding it to list of visited cells
        # else:
        #     cc = stack.pop(0)
            
                
        # moving up to the new block
        # if num_of_paths > 0:
        #     nn = list(reversed(nb))
        #     while ns != 0:
        #         n = nn.pop(0)
        #         if hunt == 'north':
                    
        #             # if we moving up, all we have to do is add 1
        #             if n - cc == 1: 
        #                 if cells[n - 1] not in visit and cells[n-1] not in obs:
        #                     cc = n-1
        #                     moved = True
        #                     break
                        
        #             if len(nn) == 1:
        #                 if cells[n] not in visit and cells[n] not in obs:
        #                     cc = n
        #         else:
        #             continue
        # else:
        #     blocked = True    
        
    
        
        
        pass 
        
    print('Execution done')
    turtle.mainloop()