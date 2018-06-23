# ----------
# User Instructions:
#
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------
from pip.wheel import open_for_csv
from pip.commands import search

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']


def search(grid,init,goal,cost):
    init_list = [0, init[0], init[1]]
    print "initial open list:"
    print "    ", init_list
    print "----"

    open_list = []
    open_list.append(init_list)

    # check the grid we are at
    grid[init[0]][init[1]] = 1
    # use open_list as priority stack
    while len(open_list) > 0:
        print "take list item"
        the_line = open_list[0]
        print the_line
        del open_list[0]
        # check around and add if they are available
        if the_line[1] > 0 and grid[the_line[1]-1][the_line[2]] == 0:
            # create the line for upper pos and add it to open_list
            up = [the_line[0] + 1, the_line[1] - 1, the_line[2]]            
            open_list.append(up)
            # make the upper position 1
            grid[the_line[1] - 1][the_line[2]] = 1
            # check if the added position is the goal
            if checkGoal(up, goal):
                return up

        if the_line[2] > 0 and grid[the_line[1]][the_line[2]-1] == 0:
            left = [the_line[0] + 1, the_line[1], the_line[2] -1]
            open_list.append(left)
            grid[the_line[1]][the_line[2] - 1] = 1
            if checkGoal(left, goal):
                return left
        if the_line[1] < len(grid) - 1 and grid[the_line[1] + 1][the_line[2]] == 0:
            down = [the_line[0] + 1, the_line[1] + 1, the_line[2]]
            open_list.append(down)
            grid[the_line[1] + 1][the_line[2]] = 1
            if checkGoal(down, goal):
                return down
        if the_line[2] < len(grid[0]) - 1 and grid[the_line[1]][the_line[2] + 1] == 0:
            right = [the_line[0] + 1, the_line[1], the_line[2] + 1]
            open_list.append(right)
            grid[the_line[1]][the_line[2] + 1] = 1
            if checkGoal(right, goal):
                return right
        
        if len(open_list) > 1:
            sorted(open_list, key = getKey)

        print "new open list:"
        print open_list
        print "-----"

    return 'fail'

def getKey(item):
    return item[0]

def checkGoal(line, goal):
    if line[1] == goal[0] and line[2] == goal[1]:
        return True
    else:
        return False

search(grid, init, goal, cost)
