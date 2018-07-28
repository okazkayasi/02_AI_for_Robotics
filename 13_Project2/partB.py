#
# === Introduction ===
#
# In this problem, you will again build a planner that helps a robot
#   find the best path through a warehouse filled with boxes
#   that it has to pick up and deliver to a dropzone. Unlike Part A,
#   however, in this problem the robot is moving in a continuous world
#   (albeit in discrete time steps) and has constraints on the amount
#   it can turn its wheels in a given time step.
# 
# Your file must be called `partB.py` and must have a class
#   called `DeliveryPlanner`.
# This class must have an `__init__` function that takes five 
#   arguments: `self`, `warehouse`, `todo`, `max_distance`, and
#   `max_steering`.
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
# '.' (period) : traversable space.
# '#' (hash) : a wall. If the robot contacts a wall space, it will crash.
# '@' (dropzone): the space where all boxes must be delivered. The dropzone may be traversed like 
#   a '.' space.
#
# Each space is a 1 x 1 block. The upper-left corner of space warehouse[i][j] is at the point (j,-i) in
#   the plane. Spaces outside the warehouse are considered walls; if any part of the robot leaves the 
#   warehouse, it will be considered to have crashed into the exterior wall of the warehouse.
# 
# For example, 
#   warehouse = ['.#.',
#                '.#.',
#                '..@']
#   is a 3x3 warehouse. The dropzone is at space (2,-2) and there are walls at spaces (1,0) 
#   and (1,-1). The rest of the warehouse is empty space.
#
# The robot is a circle of radius 0.25. The robot begins centered in the dropzone space.
#   The robot's initial bearing is 0.
#
# The argument `todo` is a list of points representing the center point of each box.
#   todo[0] is the first box which must be delivered, followed by todo[1], and so on.
#   Each box is a square of size 0.2 x 0.2. If the robot contacts a box, it will crash.
#
# The arguments `max_distance` and `max_steering` are parameters constraining the movement
#   of the robot on a given time step. They are described more below.
#
# === Rules for Movement ===
#
# - The robot may move any distance between 0 and `max_distance` per time step.
# - The robot may set its steering angle anywhere between -`max_steering` and 
#   `max_steering` per time step. A steering angle of 0 means that the robot will
#   move according to its current bearing. A positive angle means the robot will 
#   turn counterclockwise by `steering_angle` radians; a negative steering_angle 
#   means the robot will turn clockwise by abs(steering_angle) radians.
# - Upon a movement, the robot will change its steering angle instantaneously to the 
#   amount indicated by the move, and then it will move a distance in a straight line in its
#   new bearing according to the amount indicated move.
# - The cost per move is 1 plus the amount of distance traversed by the robot on that move.
#
# - The robot may pick up a box whose center point is within 0.5 units of the robot's center point.
# - If the robot picks up a box, it incurs a total cost of 2 for that move (this already includes 
#   the 1-per-move cost incurred by the robot).
# - While holding a box, the robot may not pick up another box.
# - The robot may put a box down at a total cost of 1.5 for that move. The box must be placed so that:
#   - The box is not contacting any walls, the exterior of the warehouse, any other boxes, or the robot
#   - The box's center point is within 0.5 units of the robot's center point
# - A box is always oriented so that two of its edges are horizontal and the other two are vertical.
# - If a box is placed entirely within the '@' space, it is considered delivered and is removed from the 
#   warehouse.
# - The warehouse will be arranged so that it is always possible for the robot to move to the 
#   next box on the todo list without having to rearrange any other boxes.
#
# - If the robot crashes, it will stop moving and incur a cost of 100*distance, where distance
#   is the length it attempted to move that move. (The regular movement cost will not apply.)
# - If an illegal move is attempted, the robot will not move, but the standard cost will be incurred.
#   Illegal moves include (but are not necessarily limited to):
#     - picking up a box that doesn't exist or is too far away
#     - picking up a box while already holding one
#     - putting down a box too far away or so that it's touching a wall, the warehouse exterior, 
#       another box, or the robot
#     - putting down a box while not holding a box
#
# === Output Specifications ===
#
# `plan_delivery` should return a LIST of strings, each in one of the following formats.
#
# 'move {steering} {distance}', where '{steering}' is a floating-point number between
#   -`max_steering` and `max_steering` (inclusive) and '{distance}' is a floating-point
#   number between 0 and `max_distance`
# 
# 'lift {b}', where '{b}' is replaced by the index in the list `todo` of the box being picked up
#   (so if you intend to lift box 0, you would return the string 'lift 0')
#
# 'down {x} {y}', where '{x}' is replaced by the x-coordinate of the center point of where the box
#   will be placed and where '{y}' is replaced by the y-coordinate of that center point
#   (for example, 'down 1.5 -2.9' means to place the box held by the robot so that its center point
#   is (1.5,-2.9)).
#
# === Grading ===
# 
# - Your planner will be graded against a set of test cases, each equally weighted.
# - Each task will have a "baseline" cost. If your set of moves results in the task being completed
#   with a total cost of K times the baseline cost, you will receive 1/K of the credit for the
#   test case. (Note that if K < 1, this means you earn extra credit!)
# - Otherwise, you will receive no credit for that test case. This could happen for one of several 
#   reasons including (but not necessarily limited to):
#   - plan_delivery's moves do not deliver the boxes in the correct order.
#   - plan_delivery's output is not a list of strings in the prescribed format.
#   - plan_delivery does not return an output within the prescribed time limit.
#   - Your code raises an exception.
#
# === Additional Info ===
# 
# - You may add additional classes and functions as needed provided they are all in the file `partB.py`.
# - Your partB.py file must not execute any code when it is imported. 
# - Upload partB.py to Project 2 on T-Square in the Assignments section. Do not put it into an 
#   archive with other files.
# - Ask any questions about the directions or specifications on Piazza.
#

import StringIO
import copy
from heapq import heappush, heappop
from copy import deepcopy
import math
from math import *


class DeliveryPlanner:

    warehouse = []
    todo = []
    droploc = []
    robotloc = []
    heading = radians(0)
    max_distance = 0
    max_steering = 0

    def __init__(self, warehouse, todo, max_distance, max_steering):
        self.heading = radians(0)
        self.max_distance = max_distance
        self.max_steering = max_steering

        row_num = len(warehouse[0]) * 2 + 1
        
        start_row = ['#' for chars in range(row_num) ]
        the_warehouse = [start_row]
        for line in warehouse:
            nl = ['#']
            listed = list(line)
            for i in range(len(listed)-1):

                # write the center and the next line
                if listed[i] != '#':
                    nl.append('.')

                    if listed[i+1] != '#':
                        nl.append('.')
                    else:
                        nl.append('#')
                else:
                    nl.extend(['#', '#'])

            if listed[-1] != '#':
                nl.append('.')          
            else:
                nl.append('#')
            nl.append('#')
            the_warehouse.append(nl)
        the_warehouse.append(start_row)

        # let's add the intermediate rows

        row_num = range(1, len(the_warehouse)-1)
        last = the_warehouse[:1]
        for i in row_num:
            last.append(the_warehouse[i])
            listed = []
            for j in range(len(the_warehouse[i])):
                if the_warehouse[i][j] == '.' and the_warehouse[i+1][j] == '.':
                    listed.append('.')
                else:
                    listed.append('#')
            last.append(listed)


        # add the boxes
        for i in range(len(todo)):
            y = int(todo[i][0] * 2)
            x = int(todo[i][1] * -2)
            last[x][y] = str(i)
            self.todo.append(str(i))

        # add the droploc
        drop_x, drop_y = index_2d(warehouse, '@')
        drop_x = drop_x*2+1
        drop_y = drop_y*2+1

        last[int(drop_x)][int(drop_y)] = '@'     
        self.droploc = [drop_x, drop_y]
        self.warehouse = last
        self.robotloc = [drop_x, drop_y]
        

    def plan_delivery(self):
        

        student_planner = PartA_DeliveryPlanner(copy.copy(self.warehouse), copy.copy(self.todo))
        action_list = student_planner.plan_delivery()
        
        nodes = self.action_reader(action_list)

        straight_lines = self.road_maker(nodes)

        # # Sample of what a moves list should look like - replace with your planner results

        # moves = ['move 1.570963 2.0',   # rotate and move north 2 spaces
        #          'move 1.570963 0.1',   # rotate west and move closer to second box
        #          'lift 1',              # lift the second box
        #          'move 0.785398 1.5',   # rotate to sw and move down 1.5 squares
        #          'down 3.5 -4.0',       # set the box out of the way
        #          'move -0.785398 2.0',  # rotate to west and move 2.5 squares
        #          'move -1.570963 2.7',  # rotate to north and move to pick up box 0
        #          'lift 0',              # lift the first box
        #          'move -1.570963 0.0',  # rotate to the south east
        #          'move -0.785398 1.0',  # finish rotation
        #          'move 0.785398 2.5',   # rotate to east and move
        #          'move -1.570963 2.5',  # rotate and move south
        #          'down 4.5 -4.5',       # set down the box in the dropzone
        #          'move -1.570963 0.6',  # rotate to west and move towards box 1
        #          'lift 1',              # lift the second box
        #          'move 1.570963 0.0',   # rotate north
        #          'move 1.570963 0.6',   # rotate east and move back towards dropzone
        #          'down 4.5 -4.5']       # deliver second box

        # return moves

    # the point is not to hit walls here
    def road_maker(self, nodes):
        # start checking from first to last
        for road in nodes:
            # see if it is a list
            try:
                road + []
                lines = self.straighter(road)
                line_road = self.line_to_road(lines)
                a = 1+1
            except TypeError:
                l = False
            

    def line_to_road(self, lines):
        squ = []
        for line in lines:
            ##### the turning

            y_diff = line[1][0] - line[0][0]
            x_diff = line[1][1] - line[0][1]
            head = self.heading
            req_head = math.atan2(y_diff, x_diff)

            # calculate the turn
            diff = 0 
            if req_head < 0 and head < 0:
                diff = head - req_head
            elif req_head < 0 and head > 0:
                diff = head - req_head
                if diff > math.pi:
                    diff = -math.pi*2 + diff
            elif req_head > 0 and head < 0:
                diff = head - req_head
                if diff < - math.pi:
                    diff = math.pi*2 + diff
            else: # both positive
                diff = head - req_head

            robot_y = self.robotloc[0]
            robot_x = self.robotloc[1]

            while abs(diff) > self.max_steering:
                if diff < 0:
                    move = 'move {} {}'.format(-self.max_steering, 0)
                    self.heading = (self.heading + self.max_steering)%(2*pi)
                    diff += self.max_steering
                else:
                    move = 'move {} {}'.format(self.max_steering, 0)
                    diff -= self.max_steering
                    self.heading = (self.heading - self.max_steering)%(2*pi)
                if self.heading > radians(180):
                    self.heading = -(radians(360) - self.heading)
                squ.append(move)

            #### the moving
            distance = ((y_diff**2 + x_diff**2)**0.5)/2
            while distance > self.max_distance:
                move = 'move {} {}'.format(diff, distance)
                self.heading = (self.heading - diff)%(2*pi)
                if self.heading > radians(180):
                    self.heading = -(radians(360) - self.heading)

                robot_x += distance*cos(self.heading)
                robot_y += distance*sin(self.heading)

                diff -= 0
                distance -= self.max_distance
                squ.append(move)
            
            move = 'move {} {}'.format(diff, distance)
            self.heading = (self.heading - diff)%(2*pi)
            if self.heading > radians(180):
                self.heading = -(radians(360) - self.heading)
            robot_x += distance*2*cos(self.heading)
            robot_y += distance*2*sin(self.heading)
            self.robotloc = [robot_y, robot_x]

            squ.append(move)
        return squ



    def straighter(self, road):
        # check how long straight
        lines = []
        at = 0
        line_s = road[at]
        line_e = road[at + 1]
        x = road[at+1][0] - road[at][0]  
        y = road[at+1][1] - road[at][1]

        at += 1
        while at < len(road) - 1:
            x_check = road[at+1][0] - road[at][0]  
            y_check = road[at+1][1] - road[at][1]
            
            if x == x_check and y == y_check:
                line_e = road[at + 1]
                at += 1
            else:
                lines.append((line_s, line_e))
                x = x_check
                y = y_check
                line_s = road[at]
                line_e = road[at + 1]
                at += 1

            if at == len(road)-1:
                lines.append((line_s, line_e))
        return lines


    def action_reader(self, action_list):
        seques = []
        part = []
        rob = tuple(self.robotloc)
        # part.append(rob)
        for each in action_list:
            if each [:4] == 'move':
                x = each [-3]
                y = each [-1]
                x = int(x)
                y = int(y)
                part.append((x,y))
            else:
                
                seques.append(part)
                part = []
                seques.append(each)
        return seques


def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))


class PartA_DeliveryPlanner:
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
        # set all values to 999
        self.value = [[9999999 for col in range(len(self.warehouse[0]))] for row in range(len(self.warehouse))]

        # set visited
        self.visited = [[False for col in range(len(self.warehouse[0]))] for row in range(len(self.warehouse))]





        # robot starts at the drop location
        loc = index_2d(self.warehouse, '@')
        self.robot_loc = [loc[0], loc[1]]
        self.drop_loc = [loc[0], loc[1]]
        self.todo = todo
        self.drop_g_score = self.g_score_calc(self.drop_loc)
       # self.plan_delivery()


    def plan_delivery(self):
        moves = []
        print self.todo

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
            moves.append('down {} {}'.format(self.drop_loc[0]-1, self.drop_loc[1]-1))



 #'''       moves = ['move 2 1',
 #                'move 1 0',
 #                'lift 1',
 #                'move 2 1
 #                'down 2 2',
 #                'move 1 2',
 #                'lift 2',
 #                'down 2 2'] '''
        for i in moves:
            print i
        return moves


    def pick_the_box(self, box, step=False):

        box_index = index_2d(self.warehouse, box)

        g_score = self.g_score_calc(box_index)
        the_way = self.a_star_road(box_index, g_score)
        if not step:
            self.warehouse[box_index[0]][box_index[1]] = '.'
        return the_way

    def drop_the_box(self):

        goal = self.drop_loc
        g_score = self.drop_g_score
        if self.robot_loc == self.drop_loc:
            the_way = self.step_aside()
        else:
            the_way = self.a_star_road(goal, g_score)
        return the_way

    def step_aside(self):
        x = self.robot_loc[0]
        y = self.robot_loc[1]

        if len(self.todo) > 0:
            other_box = self.pick_the_box(self.todo[0], step=True)
            
            if len(other_box) == 0:
                return self.just_move(x, y)
            else:
                return other_box[:1]   

        return self.just_move(x, y)

    def just_move(self, x, y):     
        for i in range(len(self.pos_moves)):
            move_x = x + self.pos_moves[i][0]
            move_y = y + self.pos_moves[i][1]
            print move_x
            print move_y
            for ware in self.warehouse:
                print ware
            # it should be an empty place

            else:
                if move_x > 0 and move_y > 0 and move_x < len(self.warehouse)-1 and move_y < len(self.warehouse[0])-1:
                    if self.warehouse[move_x][move_y] == '.':
                        x = move_x - 1
                        y = move_y - 1
                        self.robot_loc = [move_x,move_y]
                        return ['move {} {}'.format(x,y)]


    def a_star_road(self, goal, g_scores):
        value = deepcopy(self.value)
        visited = deepcopy(self.visited)
        parents = [[9 for col in range(len(self.warehouse[0]))] for row in range(len(self.warehouse))]
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
                    is_goal = goal[0] == move_x or goal[1] == move_y
                    movable = self.warehouse[move_x][move_y] == '.' or self.warehouse[move_x][move_y] == '@'

                    # if it is diagonal
                    diag = True
                    if self.pos_moves[i][0] != 0 or self.pos_moves[i][1] != 0:
                        # we have to check the wall
                        # first at x 
                        x_wise =  self.warehouse[move_x][y] == '.' or self.warehouse[move_x][y] == '@'
                        y_wise = self.warehouse[x][move_y] == '.' or self.warehouse[x][move_y] == '@'
                        if x_wise and y_wise:
                            diag = True
                        else:
                            diag = False 

                    is_move = movable or is_goal

                    if is_move and diag:
                        if visited[move_x][move_y] == False and self.warehouse[move_x][move_y] != '#':
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
                                parents[move_x][move_y] = parent
                                value[move_x][move_y] = f_val
        # write the route
        route_at = list(goal)
        # last step is not needed
        goal_parent = parents[goal[0]][goal[1]]
        route_at[0] = goal[0]
        route_at[1] = goal[1]
        # route_at[0] = goal[0] + self.pos_moves[goal_parent][0]
        # route_at[1] = goal[1] + self.pos_moves[goal_parent][1]
        first = self.robot_loc[:]
        self.robot_loc = route_at[:]
        return_list = []



        # pick it up from this location

        while route_at != first:
            real_route = [i-1 for i in route_at]
            road_back = "move {} {}".format(real_route[0], real_route[1])
            parent = parents[route_at[0]][route_at[1]]
            route_at[0] = route_at[0] + self.pos_moves[parent][0]
            route_at[1] = route_at[1] + self.pos_moves[parent][1]

            return_list.insert(0, road_back)
        
        road_back = "move {} {}".format(first[0]-1, first[1]-1)
        return_list.insert(0, road_back)


        return return_list




    # this function ret,urns t0he score for a_,,star
    def g_score_calc(self, goal):
        g_scores = [[1000 for col in range(len(self.warehouse[0]))] for row in range(len(self.warehouse))]

        for i in range(1, len(self.warehouse)-1):
            for j in range(1, len(self.warehouse[0])-1):
                ver = abs(goal[0] - i)
                yatay = abs(goal[1] -j)
                diag = min(ver, yatay)
                ver -= diag
                yatay -= diag
                score = (3*diag + 2*ver + 2*yatay)
                g_scores[i][j] = score

        return g_scores

