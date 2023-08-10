
# variables tracking position and direction
#from lib2to3.pgen2.token import AT
import turtle as turt
import world.obstacles as obs
obss=False
turt.left(90)
obstacle_list =[]


position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0

def reset_globals():
    global position_y,position_x,directions,current_direction_index
    position_x = 0
    position_y = 0
    directions = ['forward', 'right', 'back', 'left']
    current_direction_index = 0

def draw_border():

    turt.penup()
    turt.goto(max_x, max_y)
    turt.pendown()
    turt.goto(min_x, max_y)
    turt.goto(min_x, min_y)
    turt.goto(max_x, min_y)
    turt.goto(max_x, max_y)
    turt.penup()
    turt.home()
    turt.setheading(90)
    #turt.pendown()

    # pass

def draw_obstacle(obsticles ):
    
    for n in obsticles:

        turt.goto(n[0],n[1])
        turt.pendown()
        turt.goto(n[0],n[1]+4)
        turt.goto(n[0]+4,n[1]+4)
        turt.goto(n[0]+4,n[1])
        turt.goto(n[0],n[1])
        turt.penup()
    turt.home()
    turt.left(90)
   


def show_position(robot_name):
    print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
    turt.goto(position_x, position_y)


#printing_obstacles()

# area limit vars
min_y, max_y = -200, 200
min_x, max_x = -100, 100

def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """
    if obs.is_position_blocked(new_x,new_y):
        return False
        
    else:
        return min_x <= new_x <= max_x and min_y <= new_y <= max_y
       

def update_position(steps):
    """
    Update the current x and y positions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """

    global position_x, position_y
    new_x = position_x
    new_y = position_y

    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps
    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps
    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps
    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps
    blocked =obs.is_path_blocked(position_x,position_y,new_x,new_y)
    allowed = is_position_allowed(new_x,new_y)
    if allowed and not blocked:
        position_x = new_x
        position_y = new_y
        
    return allowed,blocked


def do_forward(robot_name, steps):#
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    
    allowed,blocked = update_position(steps)
    if allowed and not blocked:
        turt.forward(steps)
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
    elif blocked:
        return True , "Sorry, there is an obstacle in the way."
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_back(robot_name, steps):#
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    #turt.back(steps) allowed,blocked = update_position(steps)
    allowed,blocked = update_position(-steps)
    if allowed and not blocked:
        turt.back(steps)

        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    elif blocked:
        return True , "Sorry, there is an obstacle in the way."
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'

    


def do_right_turn(robot_name):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """
    global current_direction_index

    current_direction_index += 1
    turt.right(90)
    if current_direction_index > 3:
        current_direction_index = 0

    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """
    global current_direction_index

    current_direction_index -= 1
    turt.left(90)
    if current_direction_index < 0:
        current_direction_index = 3

    return True, ' > '+robot_name+' turned left.'


def do_sprint(robot_name, steps):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """

    if steps == 1:
        return do_forward(robot_name, 1)
    else:
        (do_next, command_output) = do_forward(robot_name, steps)
        print(command_output)
        return do_sprint(robot_name, steps - 1)

