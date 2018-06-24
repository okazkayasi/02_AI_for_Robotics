# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.
# from scipy.weave.build_tools import old_arg

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid,init,goal,cost):
    value = [[[999 for row in range(len(grid[0]))] for col in range(len(grid))] for direction in range(len(forward))]


    goal_x = goal[0]
    goal_y = goal[1]

    the_list = []
    val = 0
    # for i in range(len(forward)):
        
    #     value[i][goal_x][goal_y] = val
    #     part = [val, i, goal_x, goal_y]
    #     the_list.append(part)
    part = [val, 1, goal_x, goal_y]
    the_list.append(part)
    value[1][goal_x][goal_y] = 0
    
    while(len(the_list) > 0):
        list_used = the_list[0]
        del the_list[0]
        val = list_used[0]

        # car can come to the location from 3 different direction
        for i in range(len(action)):
            direction = list_used[1]
            print "heading is ", forward_name[direction]
            # came from
            from_direction = (direction - action[i] - 2) % 4
            print 'comes from ', forward_name[from_direction]
            change_x = forward[from_direction][0]
            change_y = forward[from_direction][1]
            x = list_used[2] + change_x
            y = list_used[3] + change_y
            old_direction = (from_direction + 2) % 4
            print 'old heading ', forward_name[old_direction]

            

            if x > -1 and y > -1 and x < len(grid) and y < len(grid[0]):
                new_val = val+cost[i]
                old_val = value[old_direction][x][y]
                if grid[x][y] == 0 and new_val < old_val:
                    print 'this worked'
                    new = [val+cost[i], old_direction, x, y]
                    the_list.append(new)
                    value[old_direction][x][y] = val+cost[i]
            else:
                print 'not worked'
            
        

    policy2d = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    
    for row in range(len(value[0])):
        for col in range(len(value[0][0])):
            for direction in range(len(value)):
                min = 999
                if value[direction][row][col] < min:
                    min = value[direction][row][col]
                    policy2d[row][col] = 

                


optimum_policy2D(grid, init, goal, cost)