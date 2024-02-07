# path finder

from test_base import captured_io
from io import StringIO
from sands import robot_start, main_logic
import turtle
from sandbox import generate_maze, cell_design,neighboring_cell

# turtle knows nothing in the start of the game
# Then it travels and as it travels towards the target 

# When traveling it marks its surrounding 
# marking walls and and paths
# adding routes with multiple intersections and adding it into stack 
# We always trynna move towards the target 

# If reach a dead end, we pop out of stack...
# TO speed up this we would need to only add intersections to stack
# An intersection will be classified as a cell having two or more neighbors 

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
    
    hunt = 'north'
    h, w, cs = int(200*1.5), int(100*1.5), int(50)
    turtle.getscreen()
    
    cells = generate_maze(h,w,cs)
    obs= []
    
    for cell in cells:
        draw_obstacle(cell,'White')
    
    
    # creating obs
    for i in range(0, len(cells)-1,7):
        if i != 0:
            draw_obstacle(cells[i],'green')
            obs.append(cells[i])
            
    # for i in range(12, 26):
        
    #     if i == 15:
    #         continue
    #     # if i == 18 or i == 15:
    #     #     continue

        
    #     if i != 0:
    #         draw_obstacle(cells[i],'green')
    #         obs.append(cells[i])
        
            
    test, stack, visit ,path= [],[],[],[]
    for cell in cells:
        if cell in obs:
            test.append(cell)
            
    if len(test) == len(obs):
        print('success')
        
    cc  = 0
    path.append(cells[0])
    visit.append(cells[0])
    # ns = neighboring_cell(h*2,w*2,cs,cc)
    # ns = list(reversed(ns))
    # draw_obstacle(cells[cc],'red')
    # for n in ns:
    #     draw_obstacle(cells[n],'blue')
    
    moved = False
    
    draw_obstacle(cells[11],'pink')
    end = cells[11]

    moved = True   
    blocked = False
    
    
    # first 7 blocks
    # for i in range (0,7):
    #     visit.append(cells[i])
    #     draw_obstacle(cells[i],'brown')
    
    for i in range(8,25):
        
        draw_obstacle(cells[cc],'brown')
        nb = neighboring_cell(h*2,w*2,cs,cc)
        # # neighbors that are not part of the visited list 
        # if moved is True and cells[cc] not in obs:
        #     draw_obstacle(cells[cc],'brown')
            # nb = neighboring_cell(h*2,w*2,cs,cc)
        #     print(nb)
        #     visit.append(cells[cc])
        #     moved = False
        # for n in nb:
        #     draw_obstacle(cells[n],'yellow')
        # if blocked:
        #     print('oops no stack yet')
        #     si = stack.pop(len(stack)-1)
        #     cc = si
        #     nb = neighboring_cell(h*2,w*2,cs,cc)
        #     visit.append(cells[cc])
        #     draw_obstacle(cells[cc],'brown')
        #     blocked = False
    
        f = int (h / cs) * 2
        # registering our surrounding (r= 0, l= 1, up=2 , down=3)
        num_of_paths = 0
        
        tmp = []
        for n in nb:    # stack control
            
            if cells[n] in obs:
                print(f'This is an obs: {n}')
                # we will ignore it if it is a wall
            
            elif cells[n] not in visit and cells[n] not in obs:
                print(f'This is a path: {n}')
                tmp.append(n)
                num_of_paths += 1
                
                # if this cell has more than one path, we add it to stack right
                if num_of_paths > 1:
                    stack.append(cc)
                    print(f'added to stack: {n}')

        if len(tmp) != 0:
            tmp = sorted(tmp)
            options = [0,1,2]
            breaking = False
            while breaking is False:
                # lets try to add a weight, something called heavy maybe that dictates which direction
                # we gonna edit it to dictate which side to move
                for b in tmp:
                    
                    if len(tmp) == 1 and cells[b] not in visit:
                        cc = b
                        print('its 0 so we move')
                        visit.append(cells[cc])
                        breaking = True
                        break
                    
                    if b in options and cells[b] not in visit:
                        cc = b
                        print('its 0 so we move')
                        visit.append(cells[cc])
                        breaking = True
                        break
                    
                    if  b % cc == 1 and cells[b] not in visit:
                        cc = b
                        print('should move')
                        visit.append(cells[cc])
                        breaking = True
                        break
                    

                    if cells[b] not in visit and b > cells.index(end) and b != cc - 1:
                        cc = b
                        print('should move')
                        visit.append(cells[cc])
                        breaking = True
                        break
                    
                    
                    # if cells[b] not in visit and cells[cc+f] in obs or  cells[cc+f] in visit:
                    #     cc = b
                    #     print('should move')
                    #     visit.append(cells[cc])
                    #     breaking = True
                    #     break
                    
                    
                    
                    if cells[b] not in visit and (cc + f) == b:
                        cc = b
                        print('should move')
                        visit.append(cells[cc])
                        breaking = True
                        break
                
                # the last edit was reversing the list
                
                # adding it to list of visited cells
        else:
            cc = stack.pop(0)
            
                
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