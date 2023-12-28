# The replay module stores the functions that are essential for the replay feature
from world import world
from  test_base import captured_output

def replay(robot_name: str,command: str,user_command:list ,x:int,y: int,degree: int, history:list,turtle_variable: object,obstacle: list):
    """Replays the previous user command inputs to the robot

    Args:
        robot_name (str):The name of the robot
        command (str): The command given to the robot
        user_command (list): a list version of the command  given to the user
        x (int): The robots position on the x-axis
        y (int): The robots position on the y-axis
        degree (int): The robots orientation
        history (list): A list of commands used by user
    Returns:
        tuple: a tuple of the robots new positional values
    """

    # module is only loaded when function is called, this helps avoid circular import error
    # I am aware that this is not pep8 standard, but it recommend universaly as a last resort
    from robot import command_handler

    iteration = 0
    if not "reversed" in user_command:
        for command in history:
            x,y,degree,message,invalid_com = command_handler(robot_name,command,x,y,degree,turtle_variable,obstacle)
            iteration += 1
            coordinates = (x,y,degree)
            world.position_tracker(robot_name,coordinates,turtle_variable)

    else:
        for command in reversed(history):
            x,y,degree,message,invalid_com = command_handler(robot_name,command,x,y,degree,turtle_variable,obstacle)
            iteration += 1
            coordinates = (x,y,degree)
            world.position_tracker(robot_name,coordinates,turtle_variable)
    return x,y,degree,iteration


def range_replay(robot_name: str,command: str,user_command:list ,x:int,y: int,degree: int, history:list,start:int,stop: int,turtle_variable: object,obstacle: list):
    """Replays the previous user command inputs to the robot

    Args:
        robot_name (str):The name of the robot
        command (str): The command given to the robot
        user_command (list): a list version of the command  given to the user
        x (int): The robots position on the x-axis
        y (int): The robots position on the y-axis
        degree (int): The robots orientation
        history (list): A list of commands used by user
        start (int): The start point of the range
        stop (int): The endpoint of the range
    Returns:
        tuple: a tuple of the robots new positional values
    """
    from robot import command_handler
    # grabbing the last elements n elements of the list from point stop
    # stop is an int, it contains the number of commands you wish to replay

    iteration = 0
    if not "reversed" in user_command:
        history = history[-stop:]
        for command in history:
            x,y,degree,message,invalid_com = command_handler(robot_name,command,x,y,degree,turtle_variable,obstacle)
            iteration += 1
            coordinates = (x,y,degree)
            world.position_tracker(robot_name,coordinates,turtle_variable)
    else:
        history = history[:stop]
        for command in reversed(history):
            x,y,degree,message,invalid_com = command_handler(robot_name,command,x,y,degree,turtle_variable,obstacle)
            iteration += 1
            coordinates = (x,y,degree)
            world.position_tracker(robot_name,coordinates,turtle_variable)

    return x,y,degree,iteration

def full_range_replay(robot_name: str,command: str,user_command:list ,x:int,y: int,degree: int, history:list,start:int,stop: int,turtle_variable:object,obstacle: list):
    """Replays the previous user command inputs to the robot

    Args:
        robot_name (str):The name of the robot
        command (str): The command given to the robot
        user_command (list): a list version of the command  given to the user
        x (int): The robots position on the x-axis
        y (int): The robots position on the y-axis
        degree (int): The robots orientation
        history (list): A list of commands used by user
        start (int): The start point of the range
        stop (int): The endpoint of the range
    Returns:
        tuple: a tuple of the robots new positional values
    """
    from robot import command_handler
    # grabbing the last elements n elements of the list from point stop
    # stop is an int, it contains the number of commands you wish to replay
    
    iteration = 0
    
    if start < stop:
        history = history[-stop:-start]
        if not "reversed" in user_command:
            for command in history:
                x,y,degree,message,invalid_com = command_handler(robot_name,command,x,y,degree,turtle_variable,obstacle)
                coordinates = (x,y,degree)
                if iteration != (stop - start):
                    iteration += 1
                world.position_tracker(robot_name,coordinates,turtle_variable)
        else:
            for command in reversed(history):
                x,y,degree,message,invalid_com = command_handler(robot_name,command,x,y,degree,turtle_variable,obstacle)
                coordinates = (x,y,degree)
                if iteration != (stop - start):
                    iteration += 1
                world.position_tracker(robot_name,coordinates,turtle_variable)
    else:
        print("Improper usage of command (Proper usage: Replay 5-1).")

    return x,y,degree,iteration

def replay_com_len_2(robot_name: str,commands: tuple,x:int,y:int,degree:int,history: list,turtle_variable: object,obstacle: list):
    """
    Handles all replay commands with a length of two
    """
    
    # Replays the history in silent (replay silent)
    invalid_com = False
    command,user_command = commands

    if "silent" == user_command[1]:
        with captured_output() as (out,err):
            x,y,degree,ran = replay(robot_name,command,user_command,x,y,degree,history,turtle_variable,obstacle)
        message = replay_message_silent(robot_name,command,ran)

    # Replays the basic range in reverse (Range Reverse) 
    elif "reversed" == user_command[1]:
        x,y,degree,ran = replay(robot_name,command,user_command,x,y,degree,history,turtle_variable,obstacle)
        message = replay_message_rev(robot_name,ran)

    # Replays the range and shows output of every command being run (Replay n)
    elif user_command[1].isdigit():
        stop = int(user_command[1]) # end point of the range
        x,y,degree,ran = range_replay(robot_name,command,user_command,x,y,degree,history,0,stop,turtle_variable,obstacle)
        message = range_replay_message(robot_name,ran,command)

    else:
        message = invalid_command2(robot_name,command)
        invalid_com = True

    return x,y,degree,message,invalid_com

def replay_com_len_3(robot_name: str,commands: str,x:int,y:int,degree:int,history: list,turtle_variable: object,obstacle: list):
    """
    Handles the replay command when the length of the command is 3
    """
    invalid_com = False
    keys = ["silent","reversed"] # a list of the possible flags if the command is 3 length long


    command,user_command = commands

    if (user_command[2] in keys or  user_command[1] in keys):
        if user_command[1] == keys[0] and not user_command[2].isdigit():
            message = invalid_command2(robot_name,command)
            invalid_com = True

        # Replays the range in reverse (replay n reversed)
        elif user_command[1].isdigit() and user_command[2] == keys[1]:
            stop = int(user_command[1])
            x,y,degree,ran = range_replay(robot_name,command,user_command,x,y,degree,history,0,stop,turtle_variable,obstacle)
            message = replay_message_rev(robot_name,ran)

        # Replay Range Basic silently, used for replaying using (range n silent)
        elif user_command[1].isdigit() and user_command[2] == keys[0]:
            stop = int(user_command[1])
            with captured_output() as (out,err):
                x,y,degree,ran = range_replay(robot_name,command,user_command,x,y,degree,history,0,stop,turtle_variable,obstacle)
            message = range_replay_message(robot_name,ran,command)

        # Replays the command history in reversed silently, (Replay Reversed Silent)
        else:
            with captured_output() as (out,err):
                x,y,degree,ran = replay(robot_name,command,user_command,x,y,degree,history,turtle_variable,obstacle)
            message = replay_message_silent(robot_name,command,ran)

    # Replays the full range from a start-point to an end-point (Replay 4-2)
    elif (user_command[1].isdigit() and user_command[2].isdigit()):
        start,stop = int(user_command[2]),int(user_command[1])
        x,y,degree,ran = full_range_replay(robot_name,command,user_command,x,y,degree,history,start,stop,turtle_variable,obstacle)
        message = range_replay_message(robot_name,ran,command)
    else:
        message = invalid_command2(robot_name,command)
        invalid_com = True

    return x,y,degree,message,invalid_com


def replay_message(robot_name: str,ran):
    """Prints for the user the number of commands that was replayed

    Args:
        robot_name (str): The name of the robot
        history (list): The list containing the history of previously used commands
    """

    return (f' > {robot_name} replayed {ran} commands.')

def range_replay_message(robot_name: str,ran: int,command: str):
    """Prints for the user the number of commands that was replayed

    Args:
        robot_name (str): The name of the robot
        num_of_com (int): The number of commands to replay
        command (int): The command given to the robot
    """

    if "silent" in command:
        return (f' > {robot_name} replayed {ran} commands silently.')
    else:
        return (f' > {robot_name} replayed {ran} commands.')

def replay_message_silent(robot_name: str,command: str,ran):
    """The message displayed if the user chose to replay silently

    Args:
        robot_name (str): The name of the robot
        command (list): The command given to the robot
        history (list): list of previously use commands
    """

    # command = command_filter
    user_command = command.split(" ")
    if len(user_command) == 2 :
        return (f' > {robot_name} replayed {ran} commands silently.')
    else:
        return (f' > {robot_name} replayed {ran} commands in reverse silently.')


def replay_message_rev(robot_name: str,ran):
    """The message displayed if the user chose to replay in reverse

    Args:
        robot_name (str): The name of the robot
        ran (int): number of commands executed via replay
    """

    return (f' > {robot_name} replayed {ran} commands in reverse.')


def invalid_command2(robot_name: str,command: str):
    """Lets the user know if the command is invalid

    Args:
        robot_name (str): The name of the robot
        command (str): The command given to the robot
    """
    command_string = command
    command = command.split()
    
    
    # filtering for non_alphabetic chars in the command
    non_alpha = False
    for char in command_string:
        if char.isalpha() or char.isspace():
            continue
        else:
            non_alpha = True
            break

    if not non_alpha and len(command) < 2:
        return (f"{robot_name}: Sorry, I did not understand '{command[0].upper()} {r' '.join(command[1:])}'.")
    
    if non_alpha:
        if command_string.count("-") >= 2:
            return (f"{robot_name}: Sorry, I did not understand '{command[0].lower()} {command[1]}'.")
        else:
            return (f"{robot_name}: Sorry, I did not understand '{command[0].lower()} {command[1].upper()}'.")

    elif len(command) >= 2:
        if not "reverse" in command:
            return (f"{robot_name}: Sorry, I did not understand '{command[0].upper()} {command[1].upper()} {r' '.join(command[2:])}'.")
        else:
            return (f"{robot_name}: Sorry, I did not understand '{command[0].lower()} {(r' '.join(command[1:])).upper()}'.")
