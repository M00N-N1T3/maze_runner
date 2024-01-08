# sandbox is where i code and test my logic
import turtle
from math import modf



def draw_maze_border(height: int,width: int):
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
    # turtle.tracer(0)
    turtle.speed(10000)
    turtle.penup()
    turtle.goto(-width,height)
    # turtle.teleport(-width,height) | This will only work if you running python3 v 10.12
    turtle.pen(pensize=1,pendown=True)
    turtle.goto(width,height)
    turtle.goto(width,-height)
    turtle.goto(-width,-height)
    turtle.goto(-width,height)

    return


def square(xcord: int, ycord: int, cell_size: int):
    """
    Draws a single cell unit.
    One cell is a square of size cell_size * cell_size
    E.g if cell_size = 2, the size of the square/cell will be 2 by 2 (2h * 2w)

    Args:
        xcord (int): The corodinates of where to start drawing the cell on the x-axis
        ycord (int): The corodinates of where to start drawing the cell on the y-axis
        cell_size (int): The size of the cell
    """

    turtle.hideturtle()
    # turtle.teleport(xcord,ycord) | only works on pyhton3 v 10.12
    turtle.penup()
    turtle.goto(xcord,ycord)
    turtle.pen(pendown=True,speed=0)
    turtle.begin_poly()
    turtle.goto(xcord + cell_size,ycord)
    turtle.goto(xcord + cell_size,ycord + cell_size)
    turtle.goto(xcord,ycord + cell_size)
    turtle.goto(xcord,ycord)
    turtle.end_poly()

    # saving the created cell coordinates
    cell = list(turtle.get_poly())
    cell.pop(4)


    return tuple(cell)

def generate_cells(height: int,width: int,cell_size: int):
    """
    Generates and fills the maze with cells of a specified cell s_size

    Args:
        height (int): The height of the maze / length of y-axis
        width (int): The width of the maze / length of x-axis
        cell_size (int): The size of the cell

    cell_size also acts as the incrementing step for our print loop
    """
    height,width = height / 2, width / 2
    height,width = int(height), int(width)

    cell_ref = []
    # width is the values on our x-axis on the cartesian plain
    for x in range(-width, width, cell_size):

        # height is the values on our x-axis on the cartesian plain
        for y in range(-height + cell_size, height + cell_size, cell_size):
            # generating a single cell at a time then adding to a list of references
            cell = square(x ,y - cell_size,cell_size)
            cell_ref.append(cell)

    return cell_ref


def generate_maze(height: int, width: int, cell_size: int):
    """
    Generates a maze
    The maze is a grid containing cells/blocks of squares, of size n * n

    Args:
        height (int): Height of the maze
        width (int): Width of the maze
        cell_size (int): size of the cells
    """
    turtle.tracer(0)
    draw_maze_border(height,width)
    cell = generate_cells(height,width,cell_size)
    turtle.tracer(1)

    return cell


def paint_color(cell: list|tuple, color: list):
    """
    Fills in the color of the obstacles/path

    Args:
        cell (list | tuple): A list of all the cell coordinates
        color (list_): The color you want to paint the cells
    """
    # starting coordinates for the cell color fill
    x1,y1 = cell[0]

    turtle.tracer(0)
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(int(x1),int(y1))

    turtle.pen(pendown=False,fillcolor=color,pensize=0,pencolor=color,speed=0)
    turtle.begin_fill()
    for cord in cell[1:]:
        x,y = cord
        turtle.goto(int(x),int(y))
    turtle.goto(int(x1),int(y1))
    turtle.end_fill()

    turtle.tracer(1)
    return


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
    random_index = random.randint(0,len(stack)-1)

    # retrieving the data of the corresponding index that we popped
    index_popped = stack.pop(random_index)
    # retrieving the corresponding data's index in the list of cells
    new_index = cells.index(index_popped)

    return new_index




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


    # calculating the index of the neighboring cell to the left of the current cell
    left_neighbor = current_cell_index - factor
    neighbors.append(left_neighbor)

    # calculating the index of the neighboring cell to the top of the current cell
    if modf(current_cell_index / factor)[0] != wall_factor:
        upside_neighbor = current_cell_index + 1
        neighbors.append(upside_neighbor)

    # downside_neighbor = current_cell_index - 1
    # neighbors.append(downside_neighbor)
    if current_cell_index % factor != 0:
        downside_neighbor = current_cell_index - 1
        neighbors.append(downside_neighbor)

    # filtering out values less than zero or values greater than number of cells
    neighbors = [int(n) for n in neighbors if n < cells_total+1 and n > -1]
    # filtering out the number n if n is == to the last index in the maze grid
    neighbors = [int(n) for n in neighbors if n != cells_total]

    return neighbors


def cell_design(cell_ref: list, ele_index: int, visited_cells: list, stack: list, wall_color = 'black'):
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
    
    paint_color(cells[ele_index],wall_color)
    visited_cells.append(cells[ele_index])
    stack.append(cells[ele_index])


    def exit_pathway_clearing(maze_height: int,maze_width: int,cell_size: int, exits_ref: list, borders_ref: list):
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
            tmp +=neighboring_cell(maze_height,maze_width,cell_size,index)
        exit_entrances = [index for index in tmp if index not in borders_ref]
        
        for index in exit_entrances:
            entrance_path +=neighboring_cell(maze_height,maze_width,cell_size,index)
        entrance_path = [index for index in entrance_path if index not in exit_entrances]

        pathway_index = exit_entrances + entrance_path
        return pathway_index
        

def make_maze(maze_height: int | int = 200 , maze_width: int | int = 100, cell_size: int | int = 5 , color: str | str = 'white' ):
    """
    The main maze function, creates the maze for you

    Args:
        maze_height (int): The height of the maze
        maze_width (int): The width of the maze
        cell_size (int): The size of the maze outline lines
        color (str): The color of the obstacles in the maze
    """


    # initialization phase
    draw_maze_border(maze_height,maze_width)
    cells = generate_maze(maze_height,maze_width,cell_size)
    current_cell = random.randint(0, len(cells) -1)
    # calculating the maximum amount of cell our grid can hold
    max_cell = maze_height / cell_size * maze_width / cell_size

    # creating essentials
    stack, visited_cells, walls = [], [], []

    # creating exits and spawn spot
    center_of_maze = maze_center(cells,cell_size)
    exits, border_walls = maze_exits(cells)
    
    
    
    def exit_pathway_clearing(maze_height: int,maze_width: int,cell_size: int, exits_ref: list, borders_ref: list):
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
            tmp +=neighboring_cell(maze_height,maze_width,cell_size,index)
        exit_entrances = [index for index in tmp if index not in border_walls]
        
        for index in exit_entrances:
            entrance_path +=neighboring_cell(maze_height,maze_width,cell_size,index)
        entrance_path = [index for index in entrance_path if index not in exit_entrances]

        pathway_index = exit_entrances + entrance_path
        return pathway_index
        

    
       
    for wall in border_walls:
        if wall not in exits:
            paint_color(cells[wall],'black')
        else:
            paint_color(cells[wall],'Pink')
        visited_cells.append(cells[wall])
        stack.append(cells[wall])
        
        
    for cell in center_of_maze:
        cell_design(cells,cell,visited_cells,stack,'Pink')

        
    # starting maze generation sequence
    cell_design(cells,wall,visited_cells,stack,'Pink')
    moved = True
            
        
    while len(visited_cells) != max_cell:

        if moved:
            neighbors = neighboring_cell(maze_height,maze_width,cell_size,current_cell)
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
            cell_design(cells,neighbors_index,visited_cells,stack,color)

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


    # center_index = [walls.index(cells[cell]) and paint_color(cells[cell],color) for cell in center_of_maze if cells[cell] in walls ]
    # [walls.pop(wall) for wall in center_index if not wall == None]

    print('maze done')
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


def maze_exits(cells_ref:  list):
    """
    Generates the outside walls/barriers of our maze
    Then assigns an exit to the maze on each side of the maze

    Args:
        cells_ref (list): A list of all the cells in our maze

    Returns:
        tuple : a list of the exits and outside walls
    """

    # initialing temporary lists
    border_walls, filtering_corners, exits = [], [], []

    # retrieving the indexes of the specified walls
    left_walls = [cells_ref.index(cell) for cell in cells_ref[:f]]
    right_walls = [cells_ref.index(cell) for cell in cells_ref[-f:]]
    top_walls = [f-1 for f in range(len(cells_ref),0,-f)]
    bottom_walls = [f for f in range(0,len(cells_ref),f)]

    # combining all the generated index data
    border_walls = left_walls  + top_walls + right_walls + bottom_walls

    # filtering out and removing the corner walls
    for index in border_walls:
        if index == 0 or index == f-1:
            continue
        elif  index ==  len(cells_ref)-1 or index == len(cells_ref)-f:
            continue
        else:
            filtering_corners.append(index)



    # generating a possible exit to our maze depending on the wall side
    left_exit = [index for index in left_walls if index in filtering_corners]
    exit_1 = random.choice(left_exit)

    right_exit = [index for index in right_walls if index in filtering_corners]
    exit_2 = random.choice(right_exit)

    top_exit = [index for index in top_walls if index in filtering_corners]
    exit_3 = random.choice(top_exit)

    bottom_exit = [index for index in bottom_walls if index in filtering_corners]
    exit_4 = random.choice(bottom_exit)

    # creating our 4 exit points on the maze
    exits.append(exit_1)
    exits.append(exit_2)
    exits.append(exit_3)
    exits.append(exit_4)


    return exits, border_walls




if __name__ == '__main__':

    import random
    # turtle.getscreen()
    # turtle.getscreen().tracer(0)
    h = 400 + 40
    w = 200 + 40
    cs = 20
    cc = 8

    f = int(h / cs)
    max_cells = int( h/cs * w /cs)
    screen = turtle.getscreen()

    # calculating center of the maze
    # block 1
    generate_maze(h,w,cs)
    cells= generate_cells(h,w,cs)
    # c = maze_center(cells,cs)
    
    # draw_maze_border(h,w)
    make_maze(h,w,cs)
    # c = maze_center(cells,cs)
    # a, b = maze_exits(cells)
    a,c = maze_exits(cells)
    # for i in a:
        # paint_color(cells[i],'red')

    # for z in c:
        # paint_color(cells[z],'black')

    turtle.Turtle('turtle')

    
    
    screen.mainloop()


    # turtle.getscreen().mainloop()
