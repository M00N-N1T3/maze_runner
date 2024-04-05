import sys
from os.path import exists,join
from os import getcwd

gui_loader = sys.argv
gui_loader = [word.lower() for word in gui_loader]



maze_loader = "obstacles"

if len(gui_loader) > 2 and exists(join(getcwd(),'maze',f'{gui_loader[1]}.py')):
    maze_loader = gui_loader[2]
elif len(gui_loader) == 2 and exists(join(getcwd(),'maze',f'{gui_loader[1]}.py')):
    maze_loader = gui_loader[1]
else:
    maze_loader = 'obstacles'


obstacles_module = __import__(f'maze.{maze_loader}',fromlist=[f'{maze_loader}'])
