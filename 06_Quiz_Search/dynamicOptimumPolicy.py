# ----------
# User Instructions:
# 
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
# 
# Unnavigable cells as well as cells from which 
# the goal cannot be reached should have a string 
# containing a single space (' '), as shown in the 
# previous video. The goal cell should have '*'.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def optimum_policy(grid,goal,cost):
    
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    goal_x = goal[0]
    goal_y = goal[1]

    val = 0
    value[goal_x][goal_y] = val
    policy[goal_x][goal_y] = '*'
    grid[goal_x][goal_y] = 1
    the_list = [[val, goal_x, goal_y]]
    while len(the_list) > 0:
        list_used = the_list[0]
        del the_list[0]
        val = list_used[0]
        for i in range(len(delta)):
            x = list_used[1] + delta[i][0]
            y = list_used[2] + delta[i][1]

            if x > -1 and y > -1 and x < len(grid) and y < len(grid[0]) and grid[x][y] == 0:
                new = [val+cost, x, y]
                the_list.append(new)
                grid[x][y] = 1
                value[x][y] = val+1
                policy[x][y] = delta_name[i-2]

        the_list.sort(key=lambda x: x[0])
    return policy 

a = optimum_policy(grid, goal, cost)
for e in a:
    print e
