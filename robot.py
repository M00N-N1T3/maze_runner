from world import world
import sys
import movement_logics
import replay
import import_helper
from flood_fill import maze_runner


# Initializer, loaded text or graphical version
gui_loader = sys.argv
gui_loader = [word.lower() for word in gui_loader]
gui_loader.append('turtle')
gui_loader.append('garden_of_eden')


if 'turtle' in gui_loader:
    import turtle
    turtle_variable = turtle.Turtle()
    turtle_variable.color('brown','red')
    turtle_variable.setheading(90)
    turtle_variable.penup()
else:
    turtle_variable = None


def importer(robot_name: str):
    """
    Loads a specific maze, specified by the user
    """
    if len(gui_loader) > 2:
        maze_loader = gui_loader[2]
    else:
        maze_loader = 'obstacles'

    if len(maze_loader) <= 2:
        obstacles = import_helper.dynamic_import('maze.obstacles')
        message = f'{robot_name}: Loaded obstacles.'
    else:

        obstacles = import_helper.dynamic_import(f'maze.{maze_loader}')
        message = f'{robot_name}: Loaded {maze_loader}.'

    return obstacles, message
        

# Intro
def name_robot():
    """
    Returns:
        str: The name of the robot
    """
    robot_name = input("What do you want to name your robot? ")
    return robot_name



def greet_user(name: str):
    """Greets the user

    Args:
        name (string): name of the robot
    """
    print(f"{name}: Hello kiddo!")


# command based operations
def commands(command: str):
    """
    Checks whether the command given exists within the list of possible commands

    Args:
        command (str): The command for the robot
    Returns:
        bool : True / False signal on whether the command exists or not
    """

    # The list of possible commands
    commands = ["Off", "Help", "Forward", "Back", "Right", "Left", "Sprint","Replay",'Mazerun']

    exists = False
    if command in commands:
        exists = True

    return exists


def command_handler(robot_name,command,x,y,degree,turtle_variable,obstacle):

    # The command is split in two parts in list format [Command, Parameter]
    # in our com_n_par list, the command is always at index 0
    command = command_splitter(command)


    if "Right" in command or "Left" in command:
        x,y,degree,message,invalid_com = movement_logics.turn_logic(robot_name,command,x,y,degree,turtle_variable)
    else:
        x,y,degree,message,invalid_com = movement_logics.movement_logic(robot_name,command,x,y,degree,turtle_variable,obstacle)

    return x,y,degree,message,invalid_com


def command_entry(robot_name: str,history: list):
    """
    The entry point for the robot commands.
    User inputs the commands for the robot here
    From here the command gets passed around throughout the rest of the program

    Args:
        name (str): The name of the robot

    Returns:
        list : The list contains the command and its parameter (usually number of steps to move) if any
    """

    while True:
        # The command we wish the robot to execute
        command = input(f"{robot_name}: What must I do next? ").capitalize()
        # In this conditional we are checking whether the command given exists within our list of possible commands
        
        # The command is split in two parts in list format [Command, Parameter]
        com_n_par = command_splitter(command)

        # in our com_n_par list, the command is always at index 0
        if commands(com_n_par[0]):
            # If the command exits we break out the loop
            record_history(command,history)
            break
        else:
            print(invalid_command(robot_name,command))

    return command


def command_splitter(command: str):
    """Splits the command into two parts, command and parameter

    Args:
        command (str): command given to the robot

    Returns:
        list: the list consists of the command and its parameter if any
    """

    commands = command.split(" ")
    return commands


def command_filter(command:str):
    """Filters the command and removes the '-' in the command

    Args:
        command (str): The command

    Returns:
        _type_: The new command
    """
    if command.count("-") < 2:
        filtered = "".join([char.replace("-"," ") if char == "-" else char for char in command])
        return filtered
    else:
        return command



# Only commands
def shutdown(name: str):
    """Shuts down the robot

    Args:
        name (str): the name of the robot
    """

    # Prints a message to the user before shutting down the robot
    print(f"{name}: Shutting down..")


def help_user():
    """
    A guide for the end user
    Prints the available commands for the user
    """

    print("I can understand these commands:")
    print("OFF  - Shut down robot")
    print("HELP - provide information about commands")
    print("Forward - Moves the robot forward (Example: forward 10)")
    print("Back - Moves the robot backwards (Example: back 10)")
    print("Right - Rotates/turns the robot to the right")
    print("Left - Rotates/turns the robot to the left")
    print(
        "Sprint - Sprint gives gives the robot a short burst of speed (Example: sprint 10)"
    )
    print("Replay - Replays Previous commands and moves the robot accordingly")
    print("Replay silent - Replays Previous commands silently and moves the robot accordingly.\nNo movement message printed on Screen")
    """TODO:  add replay range """
    return


def rotation(robot_name: str, direction: str):
    """Prints a message for the specified direction the robot turned

    Args:
        robot_name (str): The name of the robot
        direction (str): The direction the robot turns
    """

    print(f" > {robot_name} turned {direction[0].lower()}.")


# Examples/Messages for user
def invalid_command(robot_name: str,command: str):
    """Lets the user know if the command is invalid

    Args:
        robot_name (str): The name of the robot
        command (str): The command given to the robot
    """

    return (f"{robot_name}: Sorry, I did not understand '{command}'.")




# replay
def record_history(command: str,history: list):
    """Records the specified commands that user inputs by appending it to 
    an external list

    Args:
        command (str): User command
        history (list): External list containing command history
    """
    remember_these = ["Forward","Back",'Right','Left','Sprint']
    return [history.append(r"".join(command)) for commands in remember_these if commands in command]


def replay_logic(robot_name: str,command: str,x:int,y:int,degree:int,history: list,turtle_variable: object,obstacle: list) :
    """Handles the logic of the replay function and the command given by the user
    

    Args:
        robot_name (str): The name of the robot
        command (str):The command given to the robot
        x (int): Position of the robot on x-axis
        y (int): Position of the robot on y-axis
        degree (int): The direction of orientation (dir robot is facing)
        history (list): The list of previously used commands by the user

    Returns:
        tuple : Returns a tuple of arg x,y,degree
    """
    command = command_filter(command).strip()
    user_command = command_splitter(command)
    
    commands = (command,user_command)
    
    # determines whether we should print the invalid message onn the replay function side
    invalid_com = False
    
    if len(user_command) < 1 or len(user_command) > 3:
        message = invalid_command(robot_name,command)
        invalid_com = True
        return x,y,degree,message,invalid_com

    if len(user_command) == 1:
        x,y,degree,ran = replay.replay(robot_name,command,user_command,x,y,degree,history,turtle_variable,obstacle)
        message = replay.replay_message(robot_name,ran)

    elif len(user_command) == 2:
        x,y,degree,message,invalid_com = replay.replay_com_len_2(robot_name,commands,x,y,degree,history,turtle_variable,obstacle)


    elif len(user_command) == 3:
        x,y,degree,message,invalid_com = replay.replay_com_len_3(robot_name,commands,x,y,degree,history,turtle_variable,obstacle)



    return x,y,degree,message,invalid_com


# main game logic
def main_logic(robot_name,turtle_variable,obstacle,exits,cells_ref,obstacles):
    # The robots axises. The at keeps track of the robots movement and position
    x, y = 0, 0
    # The degree is what keeps track of the direction that the robot is facing at any given time
    degree = 90
    # history
    history = []

    command = ""
    while True:
        # The command given to the robot

        command = command_entry(robot_name,history)
        command = command_filter(command).strip()

        if "Off" in command:
            shutdown(robot_name)
            break

        if "Help" in command:
            help_user()
            
        elif "Mazerun" in command:
            cell = obstacles.create_obstacle(x,y,4)
            current_cell = cells_ref.index(cell)
            path = maze_runner(cells_ref,exits,obstacle,current_cell,[],408,208,4,"south",turtle_variable,x,y,degree)


        elif "Replay" in command or (command.count("-") == 1):
            x,y,degree,message,invalid_com = replay_logic(robot_name,command,x,y,degree,history,turtle_variable,obstacle)
            coordinates = (x,y,degree)
            print(message)
            if not invalid_com:
                world.position_tracker(robot_name,coordinates,turtle_variable)


        else:

            # if not world.is_blocked(robot_name,(x,y,degree),obstacle,command):
            x,y,degree,message,invalid_com = command_handler(robot_name,command,x,y,degree,turtle_variable,obstacle)
            coordinates = (x,y,degree)
            if invalid_com:
                print(message)
            else:
                world.position_tracker(robot_name,coordinates,turtle_variable)



def robot_start():
    # import sandbox as obstacles
    """This is the entry function, do not change"""

    robot_name = name_robot()

    greet_user(robot_name)
    hunt = "north"
    # importing specified maze
    obstacles, maze_loaded = importer(robot_name)
    print(maze_loaded)

    obstacle, exits, cell_ref = obstacles.generate_obstacles()
    if len(obstacle) > 0:
        obs = world.show_obstacles(obstacle)
    else:
        obs = 0
    

            

    
    main_logic(robot_name,turtle_variable,obs,exits,cell_ref,obstacles)
    return





if __name__ == "__main__":
    robot_start()
