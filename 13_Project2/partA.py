#
# === Introduction ===
#
# In this problem, you will build a planner that helps a robot
#   find the best path through a warehouse filled with boxes
#   that it has to pick up and deliver to a dropzone.
# 
# Your file must be called `partA.py` and must have a class
#   called `DeliveryPlanner`.
# This class must have an `__init__` function that takes three 
#   arguments: `self`, `warehouse`, and `todo`.
# The class must also have a function called `plan_delivery` that 
#   takes a single argument, `self`.
#
# === Input Specifications ===
# 
# `warehouse` will be a list of m strings, each with n characters,
#   corresponding to the layout of the warehouse. The warehouse is an
#   m x n grid. warehouse[i][j] corresponds to the spot in the ith row
#   and jth column of the warehouse, where the 0th row is the northern
#   end of the warehouse and the 0th column is the western end.
#
# The characters in each string will be one of the following:
#
# '.' (period) : traversable space. The robot may enter from any adjacent space.
# '#' (hash) : a wall. The robot cannot enter this space.
# '@' (dropzone): the starting point for the robot and the space where all boxes must be delivered.
#   The dropzone may be traversed like a '.' space.
# [0-9a-zA-Z] (any alphanumeric character) : a box. At most one of each alphanumeric character 
#   will be present in the warehouse (meaning there will be at most 62 boxes). A box may not
#   be traversed, but if the robot is adjacent to the box, the robot can pick up the box.
#   Once the box has been removed, the space functions as a '.' space.
# 
# For example, 
#   warehouse = ['1#2',
#                '.#.',
#                '..@']
#   is a 3x3 warehouse.
#   - The dropzone is at the warehouse cell in row 2, column 2.
#   - Box '1' is located in the warehouse cell in row 0, column 0.
#   - Box '2' is located in the warehouse cell in row 0, column 2.
#   - There are walls in the warehouse cells in row 0, column 1 and row 1, column 1.
#   - The remaining five warehouse cells contain empty space.
#
# The argument `todo` is a list of alphanumeric characters giving the order in which the 
#   boxes must be delivered to the dropzone. For example, if 
#   todo = ['1','2']
#   is given with the above example `warehouse`, then the robot must first deliver box '1'
#   to the dropzone, and then the robot must deliver box '2' to the dropzone.
#
# === Rules for Movement ===
#
# - Two spaces are considered adjacent if they share an edge or a corner.
# - The robot may move horizontally or vertically at a cost of 2 per move.
# - The robot may move diagonally at a cost of 3 per move.
# - The robot may not move outside the warehouse.
# - The warehouse does not "wrap" around.
# - As described earlier, the robot may pick up a box that is in an adjacent square.
# - The cost to pick up a box is 4, regardless of the direction the box is relative to the robot.
# - While holding a box, the robot may not pick up another box.
# - The robot may put a box down on an adjacent empty space ('.') or the dropzone ('@') at a cost
#   of 2 (regardless of the direction in which the robot puts down the box).
# - If a box is placed on the '@' space, it is considered delivered and is removed from the ware-
#   house.
# - The warehouse will be arranged so that it is always possible for the robot to move to the 
#   next box on the todo list without having to rearrange any other boxes.
#
# An illegal move will incur a cost of 100, and the robot will not move (the standard costs for a 
#   move will not be additionally incurred). Illegal moves include:
# - attempting to move to a nonadjacent, nonexistent, or occupied space
# - attempting to pick up a nonadjacent or nonexistent box
# - attempting to pick up a box while holding one already
# - attempting to put down a box on a nonadjacent, nonexistent, or occupied space
# - attempting to put down a box while not holding one
#
# === Output Specifications ===
#
# `plan_delivery` should return a LIST of moves that minimizes the total cost of completing
#   the task successfully.
# Each move should be a string formatted as follows:
#
# 'move {i} {j}', where '{i}' is replaced by the row-coordinate of the space the robot moves
#   to and '{j}' is replaced by the column-coordinate of the space the robot moves to
# 
# 'lift {x}', where '{x}' is replaced by the alphanumeric character of the box being picked up
#
# 'down {i} {j}', where '{i}' is replaced by the row-coordinate of the space the robot puts 
#   the box, and '{j}' is replaced by the column-coordinate of the space the robot puts the box
#
# For example, for the values of `warehouse` and `todo` given previously (reproduced below):
#   warehouse = ['1#2',
#                '.#.',
#                '..@']
#   todo = ['1','2']
# `plan_delivery` might return the following:
#   ['move 2 1',
#    'move 1 0',
#    'lift 1',
#    'move 2 1',
#    'down 2 2',
#    'move 1 2',
#    'lift 2',
#    'down 2 2']
#
# === Grading ===
# 
# - Your planner will be graded against a set of test cases, each equally weighted.
# - If your planner returns a list of moves of total cost that is K times the minimum cost of 
#   successfully completing the task, you will receive 1/K of the credit for that test case.
# - Otherwise, you will receive no credit for that test case. This could happen for one of several 
#   reasons including (but not necessarily limited to):
#   - plan_delivery's moves do not deliver the boxes in the correct order.
#   - plan_delivery's output is not a list of strings in the prescribed format.
#   - plan_delivery does not return an output within the prescribed time limit.
#   - Your code raises an exception.
#
# === Additional Info ===
# 
# - You may add additional classes and functions as needed provided they are all in the file `partA.py`.
# - Upload partA.py to Project 2 on T-Square in the Assignments section. Do not put it into an 
#   archive with other files.
# - Your partA.py file must not execute any code when imported.
# - Ask any questions about the directions or specifications on Piazza.
#

#  W A R E H O U S E
# m strings with n character
# m by n matrix
# . -> robot may enter from anywhere
# # -> wall
# @ -> dropzone. may be entered
''' [0-9a-zA-Z] -> a box. may not be traversed.
    if the robot is adjacent to the box, the robot
    can pick it up. Once removed it is '.'
    Corner is adjacent too.
'''
# todo -> delivery sequence
# robot may move horizontally and vertically for 2 cost
# robot may move diagonally for 3 cost
# cost to pick up is 4
# put back a box for 2 cost. it may drop it to adjacent
# if box is placed at @ it is removed from map
''' return a list of moves to minimize the total cost
    each move is a string
    'move {i} {j}' -> row col
    lift {x} -> x is box's number
    down {i} {j}
'''    
#  W A R E H O U S E
# m strings with n character
# m by n matrix
# . -> robot may enter from anywhere
# # -> wall
# @ -> dropzone. may be entered
''' [0-9a-zA-Z] -> a box. may not be traversed.
    if the robot is adjacent to the box, the robot
    can pick it up. Once removed it is '.'
    Corner is adjacent too.
'''
# todo -> delivery sequence
# robot may move horizontally and vertically for 2 cost
# robot may move diagonally for 3 cost
# cost to pick up is 4
# put back a box for 2 cost. it may drop it to adjacent
# if box is placed at @ it is removed from map
''' return a list of moves to minimize the total cost
    each move is a string
    'move {i} {j}' -> row col
    lift {x} -> x is box's number
    down {i} {j}
'''    

from heapq import heappush, heappop 
from copy import deepcopy

class DeliveryPlanner:
    robot_loc = [0,0]
    drop_loc = [0,0]
    carrying = False
    warehouse = []
    todo = []
    value = []
    visited = []
    parent = []
    pos_moves = [[-1,-1],
                 [-1, 0],
                 [-1,1],
                 [0,1],
                 [1,1],
                 [1,0],
                 [1,-1],
                 [0,-1]]
    drop_g_score = []
    
    def __init__(self, warehouse, todo):
        # add walls around warehouse
        start_row = ['#' for chars in range(len(warehouse[0])+2)]
        self.warehouse = [start_row]
        for line in warehouse:
            listed = list(line)
            listed.insert(0, '#')
            listed.append('#')
            self.warehouse.append(listed)
        # also end row
        self.warehouse.append(start_row)
        print self.warehouse
        # set all values to 999
        self.value = [[9999999 for col in range(len(self.warehouse[0]))] for row in range(len(self.warehouse))]

        # set visited 
        self.visited = [[False for col in range(len(self.warehouse[0]))] for row in range(len(self.warehouse))]

        self.parent = [[9 for col in range(len(self.warehouse[0]))] for row in range(len(self.warehouse))]



        # robot starts at the drop location
        loc = index_2d(self.warehouse, '@')
        self.robot_loc = [loc[0], loc[1]]
        self.drop_loc = [loc[0], loc[1]]
        self.todo = todo
        self.drop_g_score = self.g_score_calc(self.drop_loc)
        self.plan_delivery()


    def plan_delivery(self):
        moves = []
        while len(self.todo) > 0:
            # extract the next box
            box = self.todo.pop(0)
            # go there
            moves.extend(self.pick_the_box(box))
            # lift it
            moves.append('lift {}'.format(box))
            # bring back
            moves.extend(self.drop_the_box())
            # drop it
            moves.append('down {} {}'.format(self.drop_loc[0], self.drop_loc[1]))


 
 #'''       moves = ['move 2 1',
 #                'move 1 0',
 #                'lift 1',
 #                'move 2 1
 #                'down 2 2',
 #                'move 1 2',
 #                'lift 2',
 #                'down 2 2'] '''

        return moves

    def pick_the_box(self, box):

        box_index = index_2d(self.warehouse, box)
        
        g_score = self.g_score_calc(box_index)
        the_way = self.a_star_road(box_index, g_score)
        return the_way

    def drop_the_box(self):
        
        goal = self.drop_loc
        g_score = self.drop_g_score
        the_way = self.a_star_road(goal, g_score)
        return the_way

    def a_star_road(self, goal, g_scores):
        value = deepcopy(self.value)
        visited = deepcopy(self.visited)
        start = self.robot_loc
        
        the_heap = []
        # first node -> f_val, g_val, x, y, parent
        g_val = g_scores[start[0]][start[1]]
        f_val = g_val

        value[start[0]][start[1]] = f_val

        first_node = (f_val, g_val, start[0], start[1], -1)
        heappush(the_heap, first_node)
        cur_loc = [-1, -1]
        while len(the_heap) > 0 and cur_loc != goal:
            cur_node = heappop(the_heap)
            x = cur_node[2]
            y = cur_node[3]
            cur_loc = (x, y)
            visited[x][y] = True
            for i in range(len(self.pos_moves)):               
                move_x = x + self.pos_moves[i][0]
                move_y = y + self.pos_moves[i][1]
                if move_x > 0 and move_y > 0 and move_x < len(self.warehouse)-1 and move_y < len(self.warehouse[0])-1:
                    if visited[move_x][move_y] == False and self.warehouse[move_x][move_y] != '@':
                        g_val = g_scores[move_x][move_y]
                        # get the distance of old node
                        ex_dist = cur_node[0] - cur_node[1] 
                        new_dist = ex_dist
                        if self.pos_moves[i][0] == 0 or self.pos_moves[i][1] == 0:
                            new_dist = ex_dist + 2
                        else:
                            new_dist = ex_dist + 3
                        f_val = new_dist + g_val
                        parent = (i+4) % 8
                        new_node = (f_val, g_val, move_x, move_y, parent)
                        
                        if f_val < value[move_x][move_y]:
                            heappush(the_heap, new_node)     
                
    # this function ret,urns t0he score for a_,,star
    def g_score_calc(self, goal):
        g_scores = [[1000 for col in range(len(self.warehouse[0]))] for row in range(len(self.warehouse))]
        print g_scores

        for i in range(1, len(self.warehouse[0])-1):
            for j in range(1, len(self.warehouse)-1):
                ver = abs(goal[0] - i)
                yatay = abs(goal[1] -j)
                diag = min(ver, yatay)
                ver -= diag
                yatay -= diag
                score = (3*diag + 2*ver + 2*yatay)
                g_scores[i][j] = score

        return g_scores

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))



# warehouse = ['1#2',
#              '.#.',
#              '..@']

# plan = DeliveryPlanner(warehouse, [1,2]) 

