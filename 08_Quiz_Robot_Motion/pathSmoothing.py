# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth,
# and tolerance) and returns a smooth path. The first and 
# last points should remain unchanged.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the instructor's note
# below (the equations given in the video are not quite 
# correct).
# -----------

from copy import deepcopy

# thank you to EnTerr for posting this on our discussion forum
def printpaths(path,newpath):
    for old,new in zip(path,newpath):
        print '['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']'

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

def smooth(path, weight_data = 0.0, weight_smooth = 0.1, tolerance = 0.000001):

    # Make a deep copy of path into newpath
    newpath = deepcopy(path)

    # keep updating the newpath until the TOTAL change is smaller than tolerence
    converge = False
    while not converge:
        total_change = 0.0
        for pos in range(1, len(path)-1):    
            alpha = weight_data * (path[pos][0] - newpath[pos][0])
            beta = weight_smooth * (newpath[pos+1][0] + newpath[pos-1][0] - 2*newpath[pos][0])
            hold = newpath[pos][0] + alpha + beta               
            total_change += abs(hold - newpath[pos][0])
            newpath[pos][0] = hold
            alpha = weight_data * (path[pos][1] - newpath[pos][1])
            beta = weight_smooth * (newpath[pos+1][1] + newpath[pos-1][1] - 2*newpath[pos][1])
            hold = newpath[pos][1] + alpha + beta
            total_change += abs(hold - newpath[pos][1])
            newpath[pos][1] = hold      
        if total_change < tolerance:
            converge = True
    
    
    return newpath # Leave this line for the grader!

printpaths(path,smooth(path))
