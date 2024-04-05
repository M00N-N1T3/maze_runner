from world import world
import movement_logics


def world_pos_tracker(turtle_variable):
    """
    tracks the x-axis and the y-axis position of the robot
    Then returns a message of the robots current position in the world

    Args:
        robot_name (str): The name of the robot
        turtle_variable : the turtle_name of the robot
        
    Returns:
        list: The robot's current position on the world map
        int : The robot's current degree of orientation
        string: message on the robots whereabouts
    """
    
    # retrieving the position of the turtle
    robot_position = turtle_variable.pos()
    # retrieves the degree that turtle is facing
    degree = turtle_variable.heading()
    
    # converting the returned float into int
    position = []
    for pos in robot_position:
        position.append(int(pos))
        
    # returning the message of the robots position 
    # message = f" > {robot_name} now at position {tuple(position)}."
    return position,degree



def command_splitter(command: str):
    """Splits the command into two parts, command and parameter

    Args:
        command (str): command given to the robot

    Returns:
        list: the list consists of the command and its parameter if any
    """

    commands = command.split(" ")
    return commands



def command_handler(robot_name,command,x,y,degree,turtle_variable,obstacle):

    # The command is split in two parts in list format [Command, Parameter]
    # in our com_n_par list, the command is always at index 0
    command = command_splitter(command)


    if "Right" in command or "Left" in command:
        x,y,degree,message,invalid_com = movement_logics.turn_logic(robot_name,command,x,y,degree,turtle_variable)
    else:
        x,y,degree,message,invalid_com = movement_logics.movement_logic(robot_name,command,x,y,degree,turtle_variable,obstacle)
        
    return x,y,degree, message, invalid_com


def generate_steps_command(x,y,current_degree,cell_size):
    if current_degree == 0 and x + cell_size > 100:
        command = " ".join(['Forward',f'{100 - x}'])

    elif current_degree == 180 and x - cell_size < - 100:
        command = " ".join(['Forward',f'{100 + x}'])

    elif current_degree == 90 and y + cell_size > 200:
        command = " ".join(['Forward',f'{200 - y}'])

    elif current_degree == 270 and y - cell_size < - 200:
        command = " ".join(['Forward',f'{200 + y}'])

    else:
        command = " ".join(['Forward',f'{cell_size}'])
        
    return command

def fix_degree(current_degree):


    if current_degree == -270:
        current_degree = 90
    elif current_degree == -90:
        current_degree = 270
    elif current_degree == -180:
        current_degree = 180
    elif current_degree == 360:
        current_degree = 0

    return current_degree


def rotate_robot(actual_degree, current_degree):
    """
    Calculates the number of times to turn the robot left/right
    so that it is facing the correct direction that it needs to move forward in

    Args:
        actual_degree (int): the degree the robot needs to be facing in order to move forward in the specified direction
        current_degree (int): the degree the robot is currently facing
    Returns:
        int : the number of times the robot needs to turn and in what direction (- left / + right)
    """
    
    north = [90,-270]
    south = [-90,270]
    east = [0,360]
    west = [180,-180]
    if current_degree in north:
        # the idea is if we by 90/-270 and we want to go to 180
        if actual_degree in north:
            return None
        
        if actual_degree in west:
            turn = ['Left']
        elif actual_degree in east:
            turn = ['Right']
        else:
            turn = ['Right','Right']

    
    elif current_degree in south:
        
        if actual_degree in south:
            return None

        if actual_degree in east:
            turn = ['Left']
        elif actual_degree in west:
            turn = ['Right']
        else:
            turn = ['Right','Right']
            
    elif current_degree in east:
        
        if actual_degree in east:
            return None
        
        if actual_degree in north:
            turn = ['Left']
        elif actual_degree in south:
            turn = ['Right']
        else:
            turn = ['Right','Right']
            
    else:
        
        if actual_degree in west:
            return None
        
        if actual_degree in north:
            turn = ['Right']
        elif actual_degree in south:
            turn = ['Left']
        else:
            turn = ['Right','Right']

    return turn


def find_cell(cells_ref,x,y,cell_Size):
    # not required to solve a simple maze
    return None,None,None

def maze_run(cells_ref,exit_points, obstacle_ref,current_cell,visited_cells,height,width,cells_size,hunt,turtle_variable,x,y,degree):
    # not required to solve a simple maze

    return None


# def draw_obstacle(cell: list|tuple,turtle_variable, color1: str = None,color2: str = None):
#     """
#     Fills in the color of the obstacles/path

#     Args:
#         cell (list | tuple): A list of all the cell coordinates
#         color (list_): The color you want to paint the cells
#     """
#     # starting coordinates for the cell color fill
#     import turtle
#     # unit = 1.5
#     unit = 1
#     gui_loader = ['turtle']
#     # if 'turtle' in sys.argv:
#     if 'turtle' in gui_loader:
#         x1,y1 = cell[0]

#         # turtle.tracer(0)
#         # turtle_variable.hideturtle()
#         turtle_variable.penup()
#         turtle_variable.goto(int(x1),int(y1))
#         # turtle_variable.goto(int(x1) * unit,int(y1) * unit)
#         turtle_variable.pen(pendown=True,fillcolor=color1,pensize=0,pencolor=color2,speed=0)
#         turtle_variable.begin_fill()
#         for cord in cell:
#             x,y = cord
#             turtle_variable.goto(int(x) ,int(y))
#             # turtle_variable.goto(int(x) * unit,int(y) * unit)
#         turtle_variable.goto(int(x1),int(y1))
#         # turtle_variable.goto(int(x1) * unit,int(y1) * unit)
#         turtle_variable.end_fill()

#         # turtle.tracer(1)
#     else:
#         pass

#     return None

def solve_maze(coordinates,robot_name,turtle_variable,path_taken,cells_ref,obstacles,factor, hunt = "top",cell_size = 10, unit = 1.5):
    robot_name = robot_name
    x,y,current_degree = coordinates

    targets = {"top":200, "bottom":-200, "right":100, "left":-100}
    target_degrees = {"top":90, "bottom":270, "right":0, "left":180}

    target = {target for key,target in targets.items() if hunt == key}.pop()
    target_degree = {degree for key,degree in target_degrees.items() if hunt == key}.pop()

    # # ob = ((-80,0),(-90,0),(-90,10),(-80,10))
    # ob = ((-5,-25),(5,-25),(5,-15),(-5,-15))
    
    # for ob in obstacles:
    #     draw_obstacle(ob,turtle.Turtle(),"brown")
    
 
    dodge_obstacles = None
    while True:



        turns = rotate_robot(target_degree,current_degree)

        if turns != None:
            for command in turns:
                x,y,current_degree,message,invalid = command_handler(robot_name,command,x,y,current_degree,turtle_variable,obstacles)
                coordinates=(x,y,current_degree)
                world.position_tracker(robot_name,coordinates,turtle_variable)

        command = generate_steps_command(x,y,current_degree,cell_size)
        x,y,current_degree,message,invalid = command_handler(robot_name,command,x,y,current_degree,turtle_variable,obstacles)
        coordinates=(x,y,current_degree)
        world.position_tracker(robot_name,coordinates,turtle_variable)

        if target_degree in [0,180]:
            dodge_it = x
        else:
            dodge_it = y

        # changes the direction that the robot is facing when it encounters an obstacle
        if dodge_it == dodge_obstacles and current_degree == target_degree:
            # current_degree is the current degree fo teh direction the robot is facing
            x,y,current_degree,message,invalid = command_handler(robot_name,"Right",x,y,current_degree,turtle_variable,obstacles)
            coordinates=(x,y,current_degree)
            world.position_tracker(robot_name,coordinates,turtle_variable)

            command = generate_steps_command(x,y,current_degree,10)
            x,y,current_degree,message,invalid = command_handler(robot_name,command,x,y,current_degree,turtle_variable,obstacles)
            coordinates=(x,y,current_degree)
            world.position_tracker(robot_name,coordinates,turtle_variable)

        # here we setting the dodging value (value of x/y) the same as the previous (x/y)
        # in the next iteration if these two values are equal that is how we know that we
        # have not moved forward, thus there is something blocking us (An obstacle)
        dodge_obstacles = dodge_it
        current_degree = fix_degree(current_degree)

        if target_degree == current_degree and dodge_it == target:
            return x,y,current_degree



# mazer_R("right")