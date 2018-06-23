# These import steps give you access to libraries which you may (or may
# not) want to use.
from math import *
from robot import *
from matrix import *
import random

# This is the function you have to write. The argument 'measurement' is a
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
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
#       print more and 
#       let's add more
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










def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
