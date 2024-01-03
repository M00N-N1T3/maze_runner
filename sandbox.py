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
    # turtle.teleport(-width,height) | This will only work if you runnign python3 v 10.12
    turtle.pendown()
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
    # cords = []

    turtle.hideturtle()
    turtle.speed(10000)
    # turtle.tracer(0)
    # turtle.speed(1)
    # turtle.teleport(xcord,ycord) | only works on pyhton3 v 10.12
    turtle.penup()
    turtle.goto(xcord,ycord)
    turtle.pendown()
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
    # width is the values on our x-axis on the cartesian plein
    for x in range(-width, width, cell_size):

        # height is the values on our x-axis on the cartesian plein
        for y in range(-height + cell_size, height + cell_size, cell_size):
            cell = square(x ,y - cell_size,cell_size)
            cell_ref.append(cell)

    return cell_ref


def genarate_maze(height: int, width: int, cell_size: int):
    """
    Generates a maze
    The maze is a grid containing cells/blocks of squares, of size n * n

    Args:
        height (int): Height of the maze
        width (int): Width of the maze
        cell_size (int): size of the cells
    """
    turtle.tracer(0)
    # turtle.color('black','white')
    draw_maze_border(height,width)
    cell = generate_cells(height,width,cell_size)
    
    # print(cell)
    return cell

def paint(cell):
    # turtle.teleport(int(cell[0][0]),int(cell[0][1]))
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(int(cell[0][0]),int(cell[0][1]))
    turtle.pendown()
    turtle.begin_fill()
    turtle.goto(int(cell[1][0]),int(cell[1][1]))
    turtle.goto(int(cell[2][0]),int(cell[2][1]))
    turtle.goto(int(cell[3][0]),int(cell[3][1]))
    turtle.goto(int(cell[0][0]),int(cell[0][1]))
    turtle.end_fill()




def works():
    bank = []
    count = 0
    for i in range(0,11):

        # chnages the neighboring cell
        for y in range(1,5):
            print(cells[i+y])

            # checks if the x and y pair in the main cell is in ne.cell
            for cell in cells[i]:
                if cell in cells[i+y]:
                    bank.append(cells[i])
                    bank.append(cells[i+y])
                    break
                else:
                    print('no')
            # print(cells[i+1])
            # bank.append(c)
            if len(bank) > 3:
                break

            if count == 3:
                break
            else:
                count +=1
        break

    print(bank)


    for j in bank:
        paint(j)


# algo for neighbors
# works()

# print(len(cells))

def test_1():
    paint(cells[11-8])
    paint(cells[11])
    paint(cells[11+1])
    paint(cells[11-1])
    paint(cells[11+8])

def neighbouring_cell(hieght: int,width: int,cell_size: int,current_cell_index: int) -> list:
    """
    Calculates and predicts the index(s) of neighbouring cells
    to the current cell

    Args:
        hieght (int): Height of the maze
        width (int): Width of the maze
        cell_size (int): Size / Area of a single cell block
        current_cell_index (int): The index of the current cell we are in

    Returns:
        list: a list of the available neighbours
    """

    # The total number of cells in the maze
    cells_total = hieght / cell_size * width / cell_size
    # The max number of cells we can fit in a single y-axis column
    factor = hieght / cell_size
    # bottom walls float values, we get it by dividing 1 by factor, answer = n.bw_factor
    bw_factor = modf(1 / factor)[0]

    neighbours = []
    # neighbours = [current_cell_index]


    # calculating the index of the neighbouring cell to the right of the current cell
    right_neighbour = current_cell_index + factor
    neighbours.append(right_neighbour)


    left_neighbour = current_cell_index - factor
    neighbours.append(left_neighbour)


    if current_cell_index % factor != 0:
        upside_neighbour = current_cell_index + 1
        neighbours.append(upside_neighbour)



    # downside_neighbour = current_cell_index - 1
    # neighbours.append(downside_neighbour)
    if modf(current_cell_index / factor)[0] != bw_factor:
        downside_neighbour = current_cell_index - 1
        neighbours.append(downside_neighbour)

    neighbours = [int(n) for n in neighbours if n < cells_total+1 and n > 0]

    return neighbours




if __name__ == '__main__':
    import random
    turtle.getscreen().tracer(0)
    h = 400
    w = 200
    cs = 50
    
    
    
    screen = turtle.getscreen()


    cells = genarate_maze(h,w,cs)
    neighbours = neighbouring_cell(h,w,cs,13)
    n = random.choice(neighbours)
    print(neighbours) 
    print(n)
    paint(cells[13])
    paint(cells[n])
    
    # print(n)
    # for m in n:
    #     paint(cells[int(m - 1)])

    # print(modf(4.125)[0])

    # screen.mainloop()
    turtle.getscreen().mainloop()
