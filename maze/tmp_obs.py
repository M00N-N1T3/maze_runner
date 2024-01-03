import turtle

def neighboring_cell(height: int,width: int,cell_size: int,current_cell_index: int) -> list:
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
    # The max number of cells we can fit in a single y-axis column
    factor = height / cell_size

    neighbors = [current_cell_index]


    # calculating the index of the neighboring cell to the right of the current cell
    right_neighbor = current_cell_index + factor
    neighbors.append(right_neighbor)


    left_neighbor = current_cell_index - factor
    neighbors.append(left_neighbor)


    if current_cell_index % factor != 0:
        upside_neighbor = current_cell_index + 1
        neighbors.append(upside_neighbor)

    if current_cell_index % factor > 1:
        downside_neighbor = current_cell_index - 1
        neighbors.append(downside_neighbor)

    neighbors = [n for n in neighbors if n < cells_total+1 and n > 0]

    return neighbors


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

    turtle.speed(10000)
    turtle.teleport(-width,height)
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
        xcord (int): The coordinates of where to start drawing the cell on the x-axis
        ycord (int): The coordinates of where to start drawing the cell on the y-axis
        cell_size (int): The size of the cell
    """
    # cords = []

    # turtle.hideturtle()
    turtle.speed(10000)
    # turtle.speed(1)
    turtle.teleport(xcord,ycord)
    turtle.begin_poly()
    turtle.goto(xcord + cell_size,ycord)
    turtle.goto(xcord + cell_size,ycord + cell_size)
    turtle.goto(xcord,ycord + cell_size)
    turtle.goto(xcord,ycord)
    turtle.end_poly()

    # for i in range(4):
    #     turtle.fd(cell_size)
    #     turtle.rt(90)
    #     cords.append(turtle.position())
    # cords.append(turtle.position())

    # print(cords)
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
    draw_maze_border(height,width)
    cell = generate_cells(height,width,cell_size)
    
    # print(cell)
    return cell

def paint(cell):
    turtle.teleport(int(cell[0][0]),int(cell[0][1]))
    turtle.begin_fill()
    turtle.goto(int(cell[1][0]),int(cell[1][1]))
    turtle.goto(int(cell[2][0]),int(cell[2][1]))
    turtle.goto(int(cell[3][0]),int(cell[3][1]))
    turtle.goto(int(cell[0][0]),int(cell[0][1]))
    turtle.end_fill()
