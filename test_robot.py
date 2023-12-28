import unittest
from io import StringIO
from test_base import captured_io, captured_output
from unittest.mock import patch
from robot import *
from mechanics import *
import random
from world.obstacles import *


turtle_variable = None


class Test_Pilot(unittest.TestCase):
    def test_naming_robot(self):
        with captured_io(StringIO("Ben 10'son\n")) as (out, err):
            name = name_robot()
        output = out.getvalue() + name
        expected_out = "What do you want to name your robot? Ben 10'son"
        self.assertEqual(output, expected_out)

    def test_greeting(self):
        with captured_output() as (out, err):
            greet_user("Ben 10'son")
        output = out.getvalue()
        self.assertEqual(output, "Ben 10'son: Hello kiddo!\n")

    def test_full_intro(self):
        with captured_io(StringIO("10-I-C\n")) as (out, err):
            name = name_robot()
            greet_user(name)
        expected_out = "What do you want to name your robot? 10-I-C: Hello kiddo!\n"
        output = out.getvalue()
        self.assertEqual(output, expected_out)


class Test_Powering_OFF(unittest.TestCase):
    def test_off_lowercase(self):
        robot_name = "Sl33PY"
        expected_out = f"{robot_name}: Shutting down.."

        with captured_io(StringIO("off\n")) as (out, err):
            shutdown(robot_name)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_off_uppercase(self):
        robot_name = "Sl33PY"
        expected_out = f"{robot_name}: Shutting down.."

        with captured_io(StringIO("OFF\n")) as (out, err):
            shutdown(robot_name)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_off_mixed_case1(self):
        robot_name = "Sl33PY"
        expected_out = f"{robot_name}: Shutting down.."

        with captured_io(StringIO("Off\n")) as (out, err):
            shutdown(robot_name)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_off_mixed_case2(self):
        robot_name = "Sl33PY"
        expected_out = f"{robot_name}: Shutting down.."

        with captured_io(StringIO("OFf\n")) as (out, err):
            shutdown(robot_name)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)


class Test_Help(unittest.TestCase):
    def test_help_command1(self):
        obstacle = generate_obstacles()
        robot_name = "Helper"
        expected_out = f"""{robot_name}: What must I do next? I can understand these commands:
OFF  - Shut down robot\nHELP - provide information about commands
Forward - Moves the robot forward (Example: forward 10)\nBack - Moves the robot backwards (Example: back 10)
Right - Rotates/turns the robot to the right\nLeft - Rotates/turns the robot to the left
Sprint - Sprint gives gives the robot a short burst of speed (Example: sprint 10)
Replay - Replays Previous commands and moves the robot accordingly
Replay silent - Replays Previous commands silently and moves the robot accordingly.\nNo movement message printed on Screen
{robot_name}: What must I do next? Helper: Shutting down.."""

        with captured_io(StringIO("help\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_help_command2(self):
        obstacle = generate_obstacles()
        robot_name = "Helper"
        expected_out = f"""{robot_name}: What must I do next? I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
Forward - Moves the robot forward (Example: forward 10)
Back - Moves the robot backwards (Example: back 10)
Right - Rotates/turns the robot to the right
Left - Rotates/turns the robot to the left
Sprint - Sprint gives gives the robot a short burst of speed (Example: sprint 10)
Replay - Replays Previous commands and moves the robot accordingly
Replay silent - Replays Previous commands silently and moves the robot accordingly.\nNo movement message printed on Screen
{robot_name}: What must I do next? Helper: Shutting down.."""

        with captured_io(StringIO("HELP\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_help_command3(self):
        obstacle = generate_obstacles()
        robot_name = "Helper"
        expected_out = f"""{robot_name}: What must I do next? I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
Forward - Moves the robot forward (Example: forward 10)
Back - Moves the robot backwards (Example: back 10)
Right - Rotates/turns the robot to the right\nLeft - Rotates/turns the robot to the left
Sprint - Sprint gives gives the robot a short burst of speed (Example: sprint 10)
Replay - Replays Previous commands and moves the robot accordingly
Replay silent - Replays Previous commands silently and moves the robot accordingly.\nNo movement message printed on Screen
{robot_name}: What must I do next? Helper: Shutting down.."""

        with captured_io(StringIO("Help\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(expected_out, output)


class Test_Command_list(unittest.TestCase):
    
    def test_command_entry(self):
        robot_name = "N008"
        history = []

        with captured_io(StringIO("off\n")) as (out, err):
            command_entry(robot_name,history)
        output = out.getvalue()
        expected_out = f"N008: What must I do next? "
        self.assertEqual(expected_out, output)

    def test_command_in_list_lower(self):
        robot_name = "N008"
        history = []
        
        with captured_io(StringIO("help\n")) as (out, err):
            command = command_entry(robot_name,history)
            command = command_splitter(command)
            exists = commands(command[0])
        output = out.getvalue()
        self.assertTrue(exists)

    def test_command_in_list_upper(self):
        robot_name = "N008"
        history = []
        
        with captured_io(StringIO("HELP\n")) as (out, err):
            command = command_entry(robot_name,history)
            command = command_splitter(command)
            exists = commands(command[0])
        output = out.getvalue()
        self.assertTrue(exists)

    def test_command_in_list_mixed(self):
        robot_name = "N008"
        history = []
        
        with captured_io(StringIO("heLp\n")) as (out, err):
            command = command_entry(robot_name,history)
            command = command_splitter(command)
            exists = commands(command[0])
        output = out.getvalue()
        self.assertTrue(exists)

    def test_command_not_in_list1(self):
        robot_name = "N008"

        with captured_output() as (out, err):
            exists = commands("Shout")
        output = out.getvalue()
        self.assertFalse(exists)

    def test_invalid_command_prompt(self):
        robot_name = "N008"
        history = []
        
        with captured_io(StringIO("Say something\nHelP\n")) as (out, err):
            command_entry(robot_name,history)
        expected_out = f"""{robot_name}: What must I do next? {robot_name}: Sorry, I did not understand 'Say something'.
{robot_name}: What must I do next? """
        output = out.getvalue()
        self.assertEqual(expected_out, output)


class Test_command_slicing(unittest.TestCase):
    def test_single_input(self):
        with captured_output() as (out, err):
            com_and_par = command_splitter("Try1")
        self.assertIsInstance(com_and_par, list)

    def test_command_len1(self):
        with captured_output() as (out, err):
            com_and_par = command_splitter("Try1")
        self.assertIs(len(com_and_par), 1)

    def test_double_input(self):
        with captured_output() as (out, err):
            com_and_par = command_splitter("Try1 Try2")
        self.assertIsInstance(com_and_par, list)

    def test_command_len2(self):
        with captured_output() as (out, err):
            com_and_par = command_splitter("Try1 Try2")
        self.assertIs(len(com_and_par), 2)


# Movements only
class Test_Forward_command(unittest.TestCase):
    # add to expected output

    def test_correct_input1(self):
        obstacle = generate_obstacles()
        robot_name = "Slow_mover"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_correct_input2(self):
        obstacle = generate_obstacles()
        robot_name = "Slow_mover"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 123 steps.
 > {robot_name} now at position (0,123).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 123\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_incorrect_input1(self):
        obstacle = generate_obstacles()
        robot_name = "Slow_mover"
        expected_out = f"""{robot_name}: What must I do next? Specify number of steps in digits (Example: forward 10).
{robot_name}: What must I do next?  > {robot_name} moved forward by 123 steps.\n > {robot_name} now at position (0,123).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward\nForward 123\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_incorrect_input2(self):
        obstacle = generate_obstacles()
        robot_name = "Slow_mover"
        expected_out = f"""{robot_name}: What must I do next? Specify number of steps in digits (Example: forward 10).
{robot_name}: What must I do next?  > {robot_name} moved forward by 123 steps.\n > {robot_name} now at position (0,123).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward two\nForward 123\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)



class Test_Backward_command(unittest.TestCase):
    # add to expected output

    def test_correct_input1(self):
        obstacle = generate_obstacles()
        robot_name = "Back_up"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} moved back by 5 steps.
 > {robot_name} now at position (0,5).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nBack 5\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_correct_input2(self):
        obstacle = generate_obstacles()
        robot_name = "Back_up"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 123 steps.
 > {robot_name} now at position (0,123).\n{robot_name}: What must I do next?  > {robot_name} moved back by 100 steps.
 > {robot_name} now at position (0,23).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 123\nback 100\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_incorrect_input1(self):
        obstacle = generate_obstacles()
        robot_name = "Back_up"
        expected_out = f"""{robot_name}: What must I do next? Specify number of steps in digits (Example: forward 10).
{robot_name}: What must I do next?  > {robot_name} moved forward by 100 steps.\n > {robot_name} now at position (0,100).
{robot_name}: What must I do next?  > {robot_name} moved back by 90 steps.\n > {robot_name} now at position (0,10).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward\nForward 100\nback 90\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_incorrect_input2(self):
        obstacle = generate_obstacles()
        robot_name = "Back_up"
        expected_out = f"""{robot_name}: What must I do next? Specify number of steps in digits (Example: forward 10).
{robot_name}: What must I do next?  > {robot_name} moved forward by 100 steps.\n > {robot_name} now at position (0,100).
{robot_name}: What must I do next?  > {robot_name} moved back by 90 steps.\n > {robot_name} now at position (0,10).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward two\nForward 100\nback 90\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)



class Test_Turn_Right(unittest.TestCase):
    def test_one_rotation(self):
        obstacle = generate_obstacles()
        robot_name = "Timmy Turner"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_two_rotation(self):
        obstacle = generate_obstacles()
        robot_name = "Timmy Turner"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nright\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)


class Test_Turn_Left(unittest.TestCase):
    def test_one_rotation(self):
        obstacle = generate_obstacles()
        robot_name = "Timmy Turner"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned left.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nleft\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_two_rotation(self):
        obstacle = generate_obstacles()
        robot_name = "Timmy Turner"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned left.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned left.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nleft\nleft\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)


class Test_Movement_Mechanics(unittest.TestCase):
    def test_fwd_move(self):
        robot_name = "Move-Me"
        degree, steps, x, y = 0, "20", 0, 0
        expected_out = f" > {robot_name} moved forward by {steps} steps."

        with captured_output() as (out, err):
            forward_movement(robot_name, steps, degree, x, y)
        output = out.getvalue().strip("\n")
        self.assertEqual(output, expected_out)

    def test_fwd_move_return1(self):
        robot_name = "Move-Me"
        degree, steps, x, y = 0, "20", 0, 0

        with captured_output() as (out, err):
            output = forward_movement(robot_name, steps, degree, x, y)
        self.assertIsInstance(output, int)

    def test_fwd_move_return2(self):
        robot_name = "Move-Me"
        degree, steps, x, y = 0, "20", 30, 0

        with captured_output() as (out, err):
            output = forward_movement(robot_name, steps, degree, x, y)
        self.assertEqual(output, 50)


class Test_Sprinting(unittest.TestCase):
    
    def test_sprinting_lower(self):
        obstacle = generate_obstacles()
        turtle_variable = None
        robot_name = "Sprinter"
        expected_output = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 5 steps.
 > {robot_name} moved forward by 4 steps.
 > {robot_name} moved forward by 3 steps.
 > {robot_name} moved forward by 2 steps.
 > {robot_name} moved forward by 1 steps.
 > {robot_name} now at position (0,15).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""
        
        with captured_io(StringIO('sprint 5\noff\n')) as (out,err):
            output = main_logic(robot_name,turtle_variable,obstacle)
            output = out.getvalue().strip()
        self.assertEqual(expected_output,output)

    def test_sprinting_invalid(self):
        obstacle = generate_obstacles()
        turtle_variable = None
        robot_name = "Sprinter"
        expected_output = f"""{robot_name}: What must I do next? Specify number of steps in digits (Example: sprint 10).
{robot_name}: What must I do next?  > {robot_name} moved forward by 5 steps.
 > {robot_name} moved forward by 4 steps.
 > {robot_name} moved forward by 3 steps.
 > {robot_name} moved forward by 2 steps.
 > {robot_name} moved forward by 1 steps.
 > {robot_name} now at position (0,15).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""
        
        with captured_io(StringIO('sprint\nSPRINT 5\noff\n')) as (out,err):
            output = main_logic(robot_name,turtle_variable,obstacle)
            output = out.getvalue().strip()
        self.assertEqual(expected_output,output)

    def test_sprinting_upper(self):
        obstacle = generate_obstacles()
        turtle_variable = None
        robot_name = "Sprinter"
        expected_output = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 5 steps.
 > {robot_name} moved forward by 4 steps.
 > {robot_name} moved forward by 3 steps.
 > {robot_name} moved forward by 2 steps.
 > {robot_name} moved forward by 1 steps.
 > {robot_name} now at position (0,15).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""
        
        with captured_io(StringIO('SPRINT 5\noff\n')) as (out,err):
            output = main_logic(robot_name,turtle_variable,obstacle)
            output = out.getvalue().strip()
        self.assertEqual(expected_output,output)

    


class Test_History_Record(unittest.TestCase):
    
    
    def test_history(self):
        history = []
        words = ['forward','right','left','back']
        with captured_output() as (out,err):
            for word in words:
                record_history(word.capitalize(),history)
        self.assertEqual(len(history),4)

    def test_history_invalid(self):
        history = []
        words = ['forward','right','left','back']
        with captured_output() as (out,err):
            for word in words:
                record_history(word,history)
        self.assertEqual(len(history),0)

    def test_mixed_len(self):
        history = []
        words = ['forward','look','see','back']
        with captured_output() as (out,err):
            for word in words:
                record_history(word.capitalize(),history)
        self.assertEqual(len(history),2)
        

    def test_mixed_com(self):
        history = []
        words = ['forward','look','see','back']
        with captured_output() as (out,err):
            for word in words:
                record_history(word.capitalize(),history)
        self.assertIn(words[0].capitalize(),history)
        
class Test_Replay(unittest.TestCase):
    
    def test_replay(self):
        random.randint = lambda a,b : 0
        obstacle = generate_obstacles()
        robot_name = "Replayer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (10,10).\n > {robot_name} turned right.\n > {robot_name} now at position (10,10).
 > {robot_name} replayed 2 commands.\n > {robot_name} now at position (10,10).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nreplay\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
        
    def test_replay_reversed(self):
        obstacle = generate_obstacles()
        robot_name = "Replayer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n > {robot_name} moved forward by 10 steps.\n > {robot_name} now at position (0,0).
 > {robot_name} replayed 2 commands in reverse.\n > {robot_name} now at position (0,0).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nreplay reversed\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
    
    def test_replay_3_1_invalid(self):
        random.randint = lambda a,b : 0
        obstacle = generate_obstacles()
        robot_name = "Replayer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next? {robot_name}: Sorry, I did not understand 'Wrong'.
{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (10,10).\n > {robot_name} turned right.\n > {robot_name} now at position (10,10).
 > {robot_name} replayed 2 commands.\n > {robot_name} now at position (10,10).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nwrong\nreplay\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
    
    def test_replay_silent(self):
        random.randint = lambda a,b : 0
        obstacle = generate_obstacles()
        robot_name = "Replayer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} replayed 2 commands silently.
 > {robot_name} now at position (10,10).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nreplay silent\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
        
    def test_replay_reversed_silent(self):
        obstacle = generate_obstacles()
        robot_name = "Replayer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} replayed 2 commands in reverse silently.
 > {robot_name} now at position (0,0).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nreplay reversed silent\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
        
class Test_Replay_Range(unittest.TestCase):
    
    def test_replay_range2(self):
        obstacle = generate_obstacles()
        robot_name = "Range"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (10,10).\n > {robot_name} turned right.\n > {robot_name} now at position (10,10).
 > {robot_name} replayed 2 commands.\n > {robot_name} now at position (10,10).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nreplay 2\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
        
    def test_replay_range2_reversed(self):
        obstacle = generate_obstacles()
        robot_name = "Range"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n > {robot_name} moved forward by 10 steps.\n > {robot_name} now at position (0,0).
 > {robot_name} replayed 2 commands in reverse.\n > {robot_name} now at position (0,0).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nreplay 2 reversed\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
    
    
    def test_replay_range2_3_invalid(self):
        obstacle = generate_obstacles()
        robot_name = "Replayer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next? {robot_name}: Sorry, I did not understand 'Wrong'.
{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (10,10).\n > {robot_name} turned right.\n > {robot_name} now at position (10,10).
 > {robot_name} replayed 2 commands.\n > {robot_name} now at position (10,10).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nwrong\nreplay 2\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
    
    
    def test_replay_range2_2_invalid(self):
        obstacle = generate_obstacles()
        robot_name = "Replayer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next? {robot_name}: Sorry, I did not understand 'Wrong'.
{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (10,10).\n > {robot_name} turned right.\n > {robot_name} now at position (10,10).
 > {robot_name} replayed 2 commands.\n > {robot_name} now at position (10,10).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nwrong\nright\nreplay 2\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
    
       
    def test_replay_range_silent(self):
        obstacle = generate_obstacles()
        robot_name = "Replayer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} replayed 1 commands silently.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nreplay 1 silent\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
        
        
class Test_Replay_Full_Range(unittest.TestCase):
    
    def test_replay_range2(self):
        robot_name = "Range"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} moved forward by 20 steps.
 > {robot_name} now at position (20,10).\n{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (30,10).\n > {robot_name} turned right.\n > {robot_name} now at position (30,10).
 > {robot_name} replayed 2 commands.\n > {robot_name} now at position (30,10).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""


if __name__ == "__main__":
    unittest.main()
