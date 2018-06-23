#Program a function that returns a new distribution
#q, shifted to the right by U units. If U=0, q should
#be the same as p.


p = [[1./9, 1./9, 1./9],
     [1./9, 1./9, 1./9],
     [1./9, 1./9, 1./9]]


p = [[1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20]]


#colors = [['green', 'green', 'green'],
#          ['green', 'red',   'red'],
#          ['green', 'green', 'green']]

colors = [['red', 'green', 'green', 'red',   'red'],
          ['red', 'red',   'green', 'red',   'red'],
          ['red', 'red',   'green', 'green', 'red'],
          ['red', 'red',   'red',   'red',   'red']]



#measurements = ['red', 'red']
measurements = ['green', 'green', 'green', 'green', 'green']


#motions = [[0,0], [0,1]]
motions = [[0,0], [0,1], [1,0], [1,0], [0,1]]


sensor_right = 0.7
# when fails doesn't move at ll
p_move = 0.8



def sense(p, Z):
    q = []
    summed = 0
    for i in range(len(p)): #row
        q_row = []
        for j in range(len(p[0])): #column
            hit = (Z == colors[i][j])
            hold = (hit * sensor_right + (1-hit) * (1-sensor_right))
            q_row.append(p[i][j] * hold)
        q.append(q_row)
        summed = summed + sum(q_row)

    for i in range(len(q)):
        for j in range(len(q[0])):
            q[i][j] = q[i][j]/summed

    return q

def move(p, U):
    q = []
    for i iobn range(len(p)):
        q_row = []
        for j in range(len(p[0])):
            s = (1-p_move) * p[i][j]
            s = s + p_move * p[i - U[0] % len(p)][j - U[1] % len(p[0])]
            q_row.append(s)
        q.append(q_row)
    return q


def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'

for i in range(len(motions)):
    p = move(p, motions[i])
    p = sense(p, measurements[i])



show(p)

#for i in range(len(motions)):
#    p = sense(p, measurements[i])
#    p = move(p, motions[i])