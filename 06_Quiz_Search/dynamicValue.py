# ----------
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------
from theano.sandbox.cuda.basic_ops import row

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def compute_value(grid,goal,cost):

    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    goal_x = goal[0]
    goal_y = goal[1]

    val = 0
    value[goal_x][goal_y] = val
    grid[goal_x][goal_y] = 1
    the_list = [[val, goal_x, goal_y]]
    while len(the_list) > 0:
        list_used = the_list[0]
        del the_list[0]
        val = list_used[0]
        for direction in delta:
            x = list_used[1] + direction[0]
            y = list_used[2] + direction[1]

            if x > -1 and y > -1 and x < len(grid) and y < len(grid[0]) and grid[x][y] == 0:
                new = [val+cost, x, y]
                the_list.append(new)
                grid[x][y] = 1
                value[x][y] = val+1

        the_list.sort(key=lambda x: x[0])




    return value 

a = compute_value(grid, goal, cost)
for each in a:
    print each