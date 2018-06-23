# -----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
# 
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left, 
# up, and down motions. Note that the 'v' should be 
# lowercase. '*' should mark the goal cell.
#
# You may assume that all test cases for this function
# will have a path from init to goal.
# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid, init, goal, cost):
    path = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    expand = exp(grid, init, goal, cost)
    val = expand[goal[0]][goal[1]]
    found = False
    loc = goal[:]
    path[goal[0]][goal[1]] = '*'
    while not found:
        # check if it came from up
        if loc[0] > 0 and expand[loc[0]-1][loc[1]] == val - 1:
            val = val - 1
            loc[0] = loc[0] - 1
            path[loc[0]][loc[1]] = delta_name[2]
            if val == 0:
                return path  
        # check if it came from left
        elif loc[1] > 0 and expand[loc[0]][loc[1]-1] == val - 1:
            val = val - 1
            loc[1] = loc[1] - 1
            path[loc[0]][loc[1]] = delta_name[3]
            if val == 0:
                return path

        # check if it came from down
        elif loc[0] < len(grid) - 1 and expand[loc[0] + 1][loc[1]] == val - 1:
            val = val - 1
            loc[0] = loc[0] + 1
            path[loc[0]][loc[1]] = delta_name[0]
            if val == 0:
                return path 
        # check if it came from right
        elif loc[1] < len(grid[0]) - 1 and expand[loc[0]][loc[1] + 1] == val - 1:
            val = val - 1
            loc[1] = loc[1] + 1
            path[loc[0]][loc[1]] = delta_name[1]
            if val == 0:
                return path 
    
            
            


def exp(grid,init,goal,cost):
    init_list = [0, init[0], init[1]]
    print "initial open list:"
    print "    ", init_list
    print "----"

    open_list = []
    open_list.append(init_list)
    exp_no = 0

    # check the grid we are at
    grid[init[0]][init[1]] = 1
    expand = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    expand[init[0]][init[1]] = exp_no
    exp_no += 1
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
            # add exp_no
            if expand[the_line[1] - 1][the_line[2]] > expand[the_line[1]][the_line[2]]:
                expand[the_line[1] - 1][the_line[2]] = expand[the_line[1]][the_line[2]] + 1
            # check if the added position is the goal
            if checkGoal(up, goal):
                return expand

        if the_line[2] > 0 and grid[the_line[1]][the_line[2]-1] == 0:
            left = [the_line[0] + 1, the_line[1], the_line[2] -1]
            open_list.append(left)
            grid[the_line[1]][the_line[2] - 1] = 1
            # add exp_no
            if expand[the_line[1]][the_line[2]-1] > expand[the_line[1]][the_line[2]]:
                expand[the_line[1]][the_line[2]-1] = expand[the_line[1]][the_line[2]] + 1
            if checkGoal(left, goal):
                return expand

        if the_line[1] < len(grid) - 1 and grid[the_line[1] + 1][the_line[2]] == 0:
            down = [the_line[0] + 1, the_line[1] + 1, the_line[2]]
            open_list.append(down)
            grid[the_line[1] + 1][the_line[2]] = 1
            # add exp_no
            if expand[the_line[1] + 1][the_line[2]] > expand[the_line[1]][the_line[2]]:
                expand[the_line[1] + 1][the_line[2]] = expand[the_line[1]][the_line[2]] + 1
            if checkGoal(down, goal):
                return expand

        if the_line[2] < len(grid[0]) - 1 and grid[the_line[1]][the_line[2] + 1] == 0:
            right = [the_line[0] + 1, the_line[1], the_line[2] + 1]
            open_list.append(right)
            grid[the_line[1]][the_line[2] + 1] = 1
            # add exp_no
            if expand[the_line[1]][the_line[2]+1] > expand[the_line[1]][the_line[2]]:
                expand[the_line[1]][the_line[2]+1] = expand[the_line[1]][the_line[2]] + 1
            if checkGoal(right, goal):
                return expand
        
        if len(open_list) > 1:
            sorted(open_list, key = getKey)

        print "new open list:"
        for each in open_list:
            print "     ", each
        print "-----"

        for each in expand:
            print "     ", each
        print "----------------"

    return 'fail'

def getKey(item):
    return item[0]

def checkGoal(line, goal):
    if line[1] == goal[0] and line[2] == goal[1]:
        return True
    else:
        return False

path = search(grid, init, goal, cost)
for each in path:
    print each