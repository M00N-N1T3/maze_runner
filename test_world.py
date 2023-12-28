import unittest
from test_base import captured_output, captured_io
from world.text.world import *
from robot import main_logic
from io import StringIO
from maze.obstacles import *



turtle_variable = None
class Test_Track_Position(unittest.TestCase):
    def test_move_once_1(self):
        
        robot_name = "Here-I-Am"
        expected_out = f"> {robot_name} now at position (0,15)."
        with captured_output() as (out, err):
            position_tracker(robot_name, (0,15,90),turtle_variable)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_move_once_2(self):
        robot_name = "Here-I-Am"
        expected_out = f"> {robot_name} now at position (0,9)."
        with captured_output() as (out, err):
            position_tracker(robot_name, (0,9,90),turtle_variable)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_move_twice(self):
        obstacle = generate_obstacles()
        robot_name = "Here-I-Am"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} moved forward by 15 steps.
 > {robot_name} now at position (0,25).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("forward 10\nforward 15\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_move_fwd_right_fwd(self):
        random.randint = lambda a,b : 0
        obstacle = generate_obstacles()
        robot_name = "Here-I-Am"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} turned right.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (10,10).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Forward 10\nright\nforward 10\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)
        
        
class Test_Limit_Area(unittest.TestCase):
    def test_x_greater_than_100(self):
        obstacle = generate_obstacles()
        robot_name = "Safty-Ofiicer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next? {robot_name}: Sorry, I cannot go outside my safe zone.
 > {robot_name} now at position (0,10).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("forward 10\nforward 300\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_x_greater_than_neg_100(self):
        obstacle = generate_obstacles()
        robot_name = "Safty-Ofiicer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} moved back by 10 steps.
 > {robot_name} now at position (0,-10).\n{robot_name}: What must I do next? {robot_name}: Sorry, I cannot go outside my safe zone.
 > {robot_name} now at position (0,-10).\n{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Back 10\nBack 300\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_y_greater_200(self):
        obstacle = generate_obstacles()
        robot_name = "Safty-Ofiicer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} turned right.\n > {robot_name} now at position (0,0).
{robot_name}: What must I do next?  > {robot_name} moved forward by 10 steps.\n > {robot_name} now at position (10,0).
{robot_name}: What must I do next? {robot_name}: Sorry, I cannot go outside my safe zone.\n > {robot_name} now at position (10,0).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Right\nForward 10\nForward 300\noff\n")) as (
            out,
            err,
        ):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

    def test_y_greater_neg_200(self):
        obstacle = generate_obstacles()
        robot_name = "Safty-Ofiicer"
        expected_out = f"""{robot_name}: What must I do next?  > {robot_name} turned right.\n > {robot_name} now at position (0,0).
{robot_name}: What must I do next?  > {robot_name} moved back by 10 steps.\n > {robot_name} now at position (-10,0).
{robot_name}: What must I do next? {robot_name}: Sorry, I cannot go outside my safe zone.\n > {robot_name} now at position (-10,0).
{robot_name}: What must I do next? {robot_name}: Shutting down.."""

        with captured_io(StringIO("Right\nBack 10\nBack 300\noff\n")) as (out, err):
            main_logic(robot_name,turtle_variable,obstacle)
        output = out.getvalue().strip()
        self.assertEqual(output, expected_out)

class Test_Turn_Mechanics(unittest.TestCase):
    
    def test_dir_facing1(self):
        degree, orientation = 90, "Right"
        
        with captured_output() as (out, err):
            output = direction_facing(degree, orientation,turtle_variable)
        self.assertEqual(output, 0)

    def test_dir_facing2(self):
        degree, orientation = -180, "Right"

        with captured_output() as (out, err):
            output = direction_facing(degree, orientation,turtle_variable)
        self.assertEqual(output, -270)

    def test_dir_facing3(self):
        degree, orientation = 90, "Left"

        with captured_output() as (out, err):
            output = direction_facing(degree, orientation,turtle_variable)
        self.assertEqual(output, 180)

    def test_dir_facing4(self):
        degree, orientation = 0, "Left"

        with captured_output() as (out, err):
            output = direction_facing(degree, orientation,turtle_variable)
        self.assertEqual(output, 90)

    def test_dir_facing_return(self):
        degree, orientation = 90, "Right"

        with captured_output() as (out, err):
            output = direction_facing(degree, orientation,turtle_variable)
        self.assertIsInstance(output, int)

    def test_orientation1(self):
        with captured_output() as (out, err):
            output = orientation_filter(450)
        self.assertEqual(output, 0)

    def test_orientation2(self):
        with captured_output() as (out, err):
            output = orientation_filter(-450)
        self.assertEqual(output, 0)

class Test_ShowObstacles(unittest.TestCase):

    def test_if_obstacles_exist(self):

        obstacles = [((-33, 228), (-29, 228), (-29, 232), (-33, 232)), ((-145, 61), (-141, 61), (-141, 65), (-145, 65))]
        expected_output = f'''There are some obstacles:
- At position -33,228 (to -29,232)
- At position -145,61 (to -141,65)'''
        with captured_output() as (out,err):
            output = show_obstacles(obstacles)
            output = out.getvalue().strip()
        self.assertEqual(output,expected_output)

if __name__ == "__main__":
    unittest.main()