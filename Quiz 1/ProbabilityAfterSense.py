import numpy as np

p = [0.2, 0.2, 0.2, 0.2, 0.2]
world=['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
pHit = 0.6
pMiss = 0.2

def sense(p, Z):
    q = [0,0,0,0,0]
    for i in range(len(p)):
        if world[i] == Z:
            q[i] = p[i] * pHit
        else:
            q[i] = p[i] * pMiss
    summed = sum(q)

    for i in range(len(q)):
        q[i] = q[i]/summed
    return q


def move(p, U):
    
    return q

for k in range(len(measurements)):
    p = sense(p, measurements[k])


print p