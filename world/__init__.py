import sys

# capturing the terminal arguments, argv returns a list
gui_loader = sys.argv
gui_loader = [word.lower() for word in gui_loader]
gui_loader.append('turtle')
gui_loader.append('garden_of_eden')



# if the string in turtle is in the gui_loader, then we load the turtle world
if 'turtle' in gui_loader:
    from world.turtle import world as world
    world.draw_borders()    # drawing the constraint borders
    print('[Module] Turtle module loaded')
else:
    # if its anything else (like: text or blank)
    from world.text import world
    print('[Module] Text module loaded')



