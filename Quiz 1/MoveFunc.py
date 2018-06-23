#Program a function that returns a new distribution 
#q, shifted to the right by U units. If U=0, q should 
#be the same as p.

#p=[1./9, 1./3, 1./3, 1./9, 1./9]
#p=[1,0,0,0,0]
p = [0.2, 0.2, 0.2, 0.2, 0.2]
#world=['green', 'red', 'red', 'green', 'green']

colors = [['green', 'green', 'green'],
          ['green', 'red',   'green'],
          ['green', 'green', 'green']]

measurements = ['red', 'red']
motions = [1, 1]
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p, Z):
    q=[]
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
    return q

def move(p, U):
    q = []
    for i in range(len(p)):
        s = pExact * (p[(i-U) % len(p)])
        s = s + pOvershoot * (p[(i-U-1) % len(p)])
        s = s + pUndershoot * (p[(i-U+1) % len(p)])
        q.append(s)

    return q

for i in range(len(motions)):
    p = sense(p, measurements[i])
    p = move(p, motions[i])

print p