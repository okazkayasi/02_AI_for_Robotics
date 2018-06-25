# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# returns two grids. The first grid, value, should 
# contain the computed value of each cell as shown 
# in the video. The second grid, policy, should 
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.
from pyasn1_modules.rfc2251 import DelRequest
from Cython.Distutils.build_ext import new_build_ext
from scipy.stats._continuous_distns import wald

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    wall_value = [[collision_cost for col in range(len(grid[0])+2)] for row in range(len(grid)+2)]
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    wall_policy = [[' ' for col in range(len(grid[0])+2)] for row in range(len(grid)+2)]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    wall_grid = [[1 for col in range(len(grid[0]))] for row in range(len(grid))]
    
    # also end row
    start_row = [1 for col in range(len(grid[0]) + 2)]
    wall_grid = [start_row]
    for row in grid:
        row.insert(0,1)
        row.append(1)
        wall_grid.append(row)
    wall_grid.append(start_row)


    # we gonna need'em
    delta = [[-1, 0 ], # go up
            [ 0, -1], # go left
            [ 1, 0 ], # go down
            [ 0, 1 ]] # go right

    delta_name = ['^', '<', 'v', '>']


    # because we have wall +1
    goal_x = goal[0] + 1
    goal_y = goal[1] + 1

    wall_value[goal_x][goal_y] = 0
    wall_policy[goal_x][goal_y] = '*'
    wall_grid[goal_x][goal_y] = 1

    for i in range(100):
            
        for i in range(len(wall_grid)):
            for j in range(len(wall_grid[0])):
                if wall_grid[i][j] == 0:
                    # for each moving direction
                    for head in range(len(delta)):
                        side_prob = (1 - success_prob)/2
                        # if it is success
                        new_x = i + delta[head][0]
                        new_y = j + delta[head][1]
                        new_val = success_prob * wall_value[new_x][new_y]
                        # if it goes to one side
                        new_head = (head - 1) % len(delta) 
                        new_x = i + delta[new_head][0]
                        new_y = j + delta[new_head][1]
                        new_val += side_prob * wall_value[new_x][new_y]
                        # if it goes to the other side
                        new_head = (head + 1) % len(delta)
                        new_x = i + delta[new_head][0]
                        new_y = j + delta[new_head][1]
                        new_val += side_prob * wall_value[new_x][new_y]
                        # add one more
                        new_val += 1
                        if new_val < wall_value[i][j]:
                            wall_value[i][j] = new_val
                            wall_policy[i][j] = delta_name[head]

    # reconstruct without walls
    value = []
    policy = []
    del wall_value[0]
    del wall_value[-1]
    del wall_policy[0]
    del wall_policy[-1]
    for value_row in wall_value:
        del value_row[0]
        del value_row[-1]
        value.append(value_row)
    for policy_row in wall_policy:
        del policy_row[0]
        del policy_row[-1]
        policy.append(policy_row)

    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner
cost_step = 1
collision_cost = 1000
success_prob = 0.5

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
#[471.9397246855924, 274.85364957758316, 161.5599867065471, 0],
#[334.05159958720344, 230.9574434590965, 183.69314862430264, 176.69517762501977], 
#[398.3517867450282, 277.5898270101976, 246.09263437756917, 335.3944132514738], 
#[700.1758933725141, 1000, 1000, 668.697206625737]


#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
