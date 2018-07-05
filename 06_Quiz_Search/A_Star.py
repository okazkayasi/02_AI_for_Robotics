# -----------
# User Instructions:
#
# Modify the the search function so that it becomes
# an A* search algorithm as defined in the previous
# lectures.
#
# Your function should return the expanded grid
# which shows, for each element, the count when
# it was expanded or -1 if the element was never expanded.
# 
# If there is no path from init to goal,
# the function should return the string 'fail'
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
heuristic = [[9, 8, 7, 6, 5, 4],
             [8, 7, 6, 5, 4, 3],
             [7, 6, 5, 4, 3, 2],
             [6, 5, 4, 3, 2, 1],
             [5, 4, 3, 2, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost, heuristic):
    
    # init list: g-val, loc, f_val(g_val + heuristic)
    init_list = [0, init[0], init[1], heuristic[init[0]][init[1]]]
    print "initial open list:"
    print "    ", init_list
    print "----"

    open_list = []
    open_list.append(init_list)
    g_val = 0 
    f_val = g_val + heuristic[init[0]][init[1]]

    # check the grid we are at
    grid[init[0]][init[1]] = 1
    a_star = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    a_star[init[0]][init[1]] = g_val
    # use open_list as priority stack
    while len(open_list) > 0:
        
        print "take list item"
        the_line = open_list[0]

        print the_line
        del open_list[0]
        g_val += 1
        # check around and add if they are available
        if the_line[1] > 0 and grid[the_line[1]-1][the_line[2]] == 0:
            # create the line for upper pos and add it to open_list
            f_val = g_val + heuristic[the_line[1]-1][the_line[2]]
            up = [g_val, the_line[1] - 1, the_line[2], f_val]            
            open_list.append(up)
            # make the upper position 1
            grid[the_line[1] - 1][the_line[2]] = 1
            # add f_val
            a_star[the_line[1] - 1][the_line[2]] = g_val      
            # check if the added position is the goal
            if checkGoal(up, goal):
                return a_star
        if the_line[2] > 0 and grid[the_line[1]][the_line[2]-1] == 0:
            f_val = g_val + heuristic[the_line[1]][the_line[2]-1]
            left = [g_val, the_line[1], the_line[2] -1, f_val]
            open_list.append(left)
            grid[the_line[1]][the_line[2] - 1] = 1
            # add exp_no
            a_star[the_line[1]][the_line[2]-1] = g_val
            if checkGoal(left, goal):
                return a_star
        if the_line[1] < len(grid) - 1 and grid[the_line[1] + 1][the_line[2]] == 0:
            f_val = g_val + heuristic[the_line[1]+1][the_line[2]]
            down = [the_line[0] + 1, the_line[1] + 1, the_line[2], f_val]
            open_list.append(down)
            grid[the_line[1] + 1][the_line[2]] = 1
            # add exp_no
            a_star[the_line[1] + 1][the_line[2]] = g_val
            if checkGoal(down, goal):
                return a_star
        if the_line[2] < len(grid[0]) - 1 and grid[the_line[1]][the_line[2] + 1] == 0:
            f_val = g_val + heuristic[the_line[1]][the_line[2]+1]
            right = [the_line[0] + 1, the_line[1], the_line[2] + 1, f_val]
            open_list.append(right)
            grid[the_line[1]][the_line[2] + 1] = 1
            # add exp_no
            a_star[the_line[1]][the_line[2] + 1] = g_val
            if checkGoal(right, goal):
                return a_star
        
        if len(open_list) > 1:
            open_list = sorted(open_list, key = lambda x:(x[-1], x[0]))

        print "new open list:"
        for each in open_list:
            print "     ", each
        print "-----"

        for each in a_star:
            print "     ", each
        print "----------------"

    return 'fail'


def checkGoal(line, goal):
    if line[1] == goal[0] and line[2] == goal[1]:
        return True
    else:
        return False

a = search(grid,init,goal,cost, heuristic)
for each in a:
    print each