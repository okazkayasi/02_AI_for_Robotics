from math import *
from matrix import *
from robot import *
import random

    # This function will be called after each time the target moves. 
    # The OTHER variable is a place for you to store any historical 
    # information about the progress of the hunt (or maybe some 
    # localization information). Your must return a tuple of three 
    # values: turning, distance, OTHER

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    #Change these:
    if OTHER:
        if OTHER[0]:
            a = OTHER[0][:]
        else:
            a = []
        if OTHER[1]:
            b = OTHER[1][:]
        else:
            b = []
        if OTHER[2]:
            c = OTHER[2][:]
        else:
            c = []
        if OTHER[3]:
            d = OTHER[3][:]
        else:
            d = []
        if OTHER[4]:
            e = OTHER[4][:]
        else:
            e = []
        if OTHER[5]:
            f = OTHER[5]
        else:
            f = 0
        
        this_other = [a,b,c,d,e,f]
    else:
        this_other = None

    catch_point = False
    step = 0
    target_next = target_measurement
    turning = 0
    dist = 0
    while not catch_point:
        step += 1
        target_next, this_other = estimate_next_pos(target_next, this_other)
        dist = distance_between(hunter_position, target_next)
        turning = 0.0
        if max_distance*step > dist:
            catch_point = True
            heading_to_target = get_heading(hunter_position, target_next)
            heading_difference = heading_to_target - hunter_heading
            turning = angle_trunc(heading_difference)


    if not OTHER: # first time calling this function, set up my OTHER variables.
        OTHER = []
        distances = []
        headings = []
        locations = []
        locations.append(target_measurement)
        steps_before_turn = []
        turn_degrees = []
        step_count = 0
        OTHER.append(distances)
        OTHER.append(headings)
        OTHER.append(locations)
        OTHER.append(steps_before_turn)
        OTHER.append(turn_degrees)
        OTHER.append(step_count)

    else:
        # first get old data from OTHER
        distances = OTHER[0]
        headings = OTHER[1]
        locations = OTHER[2]
        steps_before_turn = OTHER[3]
        turn_degrees = OTHER[4]
        step_count = OTHER[5]
        step_count += 1

        # get the last distance and last heading
        distances.append(distance_between(locations[-1], target_measurement))
        dist_y = target_measurement[1] - locations[-1][1]
        dist_x = target_measurement[0] - locations[-1][0]
        head = atan2(dist_y, dist_x)
        head = angle_trunc(head)
        headings.append(head)

        # take average of distances. ignore first one.
        aver_dist = sum(distances) / (len(distances))

        # calculate the tolerance
        tolerance = 0.05*aver_dist*3

        # check if there is a difference in heading
        if len(headings) > 1:
            if abs(headings[-2] - headings[-1]) > tolerance:
                steps_before_turn.append(step_count)
                step_count = 1
                degree_turn = angle_trunc(headings[-1] - headings[-2])
                turn_degrees.append(degree_turn)

        # average turn
        average_turn = 0
        if len(turn_degrees) > 0:
            average_turn = sum(turn_degrees) / len(turn_degrees)

        # average steps so far
        average_steps = 999999
        if len(steps_before_turn) > 0:
            average_steps = sum(steps_before_turn) / len(steps_before_turn)

        # calculate new head
        if step_count > average_steps:
            new_head = angle_trunc(head + average_turn)
        else:
            new_head = head

        x = target_measurement[0] + aver_dist * cos(new_head)
        y = target_measurement[1] + aver_dist * sin(new_head)

       # add new locations
        locations.append(target_measurement)

        # reset OTHER and add all
        OTHER = []
        OTHER.append(distances)
        OTHER.append(headings)
        OTHER.append(locations)
        OTHER.append(steps_before_turn)
        OTHER.append(turn_degrees)
        OTHER.append(step_count)

    return turning, dist, OTHER


def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    if not OTHER:
        OTHER = []
        distances = []
        headings = []
        locations = []
        locations.append(measurement)
        steps_before_turn = []
        turn_degrees = []
        step_count = 0
        OTHER.append(distances)
        OTHER.append(headings)
        OTHER.append(locations)
        OTHER.append(steps_before_turn)
        OTHER.append(turn_degrees)
        OTHER.append(step_count)
#        print 'OTHER CREATED'
        return ([0,0], OTHER)

    else:
        # first get old data from OTHER
        distances = OTHER[0]
        headings = OTHER[1]
        locations = OTHER[2]
        steps_before_turn = OTHER[3]
        turn_degrees = OTHER[4]
        step_count = OTHER[5]
        step_count += 1

        # get the last distance and last heading
        distances.append(distance_between(locations[-1], measurement))
        dist_y = measurement[1] - locations[-1][1]
        dist_x = measurement[0] - locations[-1][0]
        head = atan2(dist_y, dist_x)
        head = angle_trunc(head)
        headings.append(head)

        # check if there is a difference in heading
        turn = False
        if len(headings) > 1:
            if headings[-2] != headings[-1]:
                steps_before_turn.append(step_count)
                degree_turn = angle_trunc(headings[-1] - headings[-2])
                turn_degrees.append(degree_turn)
                turn = True
#                print 'turned!!!!!!!!!!!'

        # average turn
        average_turn = 0
        if len(turn_degrees) > 0:
            average_turn = sum(turn_degrees) / len(turn_degrees)

        # average steps so far
        average_steps = 999999
        if len(steps_before_turn) > 0:
            average_steps = sum(steps_before_turn) / len(steps_before_turn)

        # take average of distances. ignore first one.
        aver_dist = sum(distances) / (len(distances))

        # calculate new head
        if step_count >= average_steps:
            new_head = angle_trunc(head + average_turn)
        else:
            new_head = head
        
        if turn:
            step_count = 0


        x = measurement[0] + aver_dist * cos(new_head)
        y = measurement[1] + aver_dist * sin(new_head)

#        print 'measurement: ', measurement
#        print 'average_turn: ', average_turn
#        print 'average steps: ', average_steps
#        print 'new_head: ', new_head
#        print 'head: ', head
#        print 'step_count', step_count

        # add new locations
        locations.append(measurement)

        # reset OTHER and add all
        OTHER = []
        OTHER.append(distances)
        OTHER.append(headings)
        OTHER.append(locations)
        OTHER.append(steps_before_turn)
        OTHER.append(turn_degrees)
        OTHER.append(step_count)
        return ([x, y]), OTHER