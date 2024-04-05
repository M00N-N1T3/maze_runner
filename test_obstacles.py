import unittest
from maze.obstacles import *
from test_base import captured_output

class Test_Obstacle(unittest.TestCase):
    
    def test_obstacle_return(self):
        with captured_output() as (out,err):
            output = create_obstacle()
        self.assertIsInstance(output,tuple)
        
    def test_num_of_elements(self):
        with captured_output() as (out,err):
            output = create_obstacle()
        self.assertEqual(len(output),4)
    
    def test_element_type(self):
        with captured_output() as (out,err):
            output = create_obstacle()
            element = output[0]
        self.assertIsInstance(element,tuple)
    
    def test_element_len(self):
        with captured_output() as (out,err):
            output = create_obstacle()
            element = output[0]
        self.assertEqual(len(element),2)
        

class Test_Obstacle_Generation(unittest.TestCase):
    
    def test_obstacle_gen(self):
        with captured_output() as (out,err):
            output = generate_obstacles()
            self.assertIsInstance(output,tuple)
    
    def test_num_obstacles(self):
        random.randint = lambda a, b: 10
        with captured_output() as (out,err):
            output = generate_obstacles()[0]
            self.assertEqual(len(output),10)
    
    def test_element_in_obstacle(self):
        random.randint = lambda a, b: 10
        with captured_output() as (out,err):
            output = generate_obstacles()[0]
            element = output[0]
            self.assertIsInstance(element,tuple)
            
    def test_element_in_len(self):
        random.randint = lambda a, b: 4
        with captured_output() as (out,err):
            output = generate_obstacles()
            element = output[0]
            self.assertEqual(len(element),4)
            
    
class Test_PositionBlocked(unittest.TestCase):
    
    def test_position_return_type(self):
        x,y = 10,25
        obstacles = [[(x,y),(x+4,y),(x+4,y+4),(x,y+4)] for i in range(2)]
        output = is_position_blocked(10,25,obstacles)
        self.assertIsInstance(output,bool)
        
    def test_position_blocked_True(self):
        x,y = 10,25
        obstacles = [[(x,y),(x+4,y),(x+4,y+4),(x,y+4)] for i in range(2)]
        output = is_position_blocked(10,25,obstacles)
        self.assertTrue(output)
        
    def test_position_blocked_False(self):
        x,y = 10,25
        obstacles = [[(x,y),(x+4,y),(x+4,y+4),(x,y+4)] for i in range(2)]
        position = 30,40
        output = is_position_blocked(30,40,obstacles)
        self.assertFalse(output)


class Test_BlockedPath(unittest.TestCase):

    def test_path_blocked_return_type(self):
        x,y = 10,25
        obstacles = [[(x,y),(x+4,y),(x+4,y+4),(x,y+4)] for i in range(2)]
        position = 10,25
        position2=path_forecast(['Forward',10],x,y,90)
        output = is_path_blocked((x,y),position2,obstacles)
        self.assertIsInstance(output,bool)

    def test_position_blocked_True(self):
        x,y = 10,25
        obstacles = [[(x,y),(x+4,y),(x+4,y+4),(x,y+4)] for i in range(2)]
        position2=path_forecast(['Forward',10],x,y,90)
        output = is_path_blocked((10,19),position2,obstacles)
        self.assertTrue(output)

    def test_position_blocked_False(self):
        x,y = 10,25
        obstacles = [[(x,y),(x+4,y),(x+4,y+4),(x,y+4)] for i in range(2)]
        init_pos = (0,0)
        position2=path_forecast(['Forward',10],0,0,90)
        output = is_path_blocked(init_pos,position2,obstacles)
        self.assertFalse(output)

class Test_PathForecast(unittest.TestCase):
    
    def test_path_forecast_return_type(self):
        x,y = 10,25
        command = ['Forward',10]
        output = path_forecast(command,x,y,90)
        self.assertIsInstance(output,tuple)
        
    def test_forecast_len(self):
        x,y = 10,25
        command = ['Forward',10]
        output = path_forecast(command,x,y,90)
        self.assertEqual(len(output),2)
        
    def test_forecast(self):
        x,y = 10,25
        command = ['Forward',10]
        output = path_forecast(command,x,y,90)
        self.assertEqual(output,(10,35))


if __name__ == '__main__':
    unittest.main()