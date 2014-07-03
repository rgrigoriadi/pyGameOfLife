# state is 2 dimension array of size X x Y

X = 10 # j
Y = 10 # i

def create_empty_state ():
    new_state = [[0]];
    for i in range(Y):
        for j in range(X):
            new_state[i].append(0)
        new_state.append([0])
    return new_state

def create_copy(state):
    copy = create_empty_state()
    for i in range(Y):
        for j in range(X):
            copy[i][j] = state[i][j]
    return copy

def get (state, y, x):
    if x >= 0 and y >= 0 and x < X and  y < Y:
        return state[y][x]
    return 0

def set (state, positions, value):
    new_state = create_copy(state)
    for pos in positions:
        x = pos[1]
        y = pos[0]
        if x >= 0 and y >= 0 and x < X and  y < Y:
            new_state[y][x] = value
    return new_state

def get_next_state(state):
    new_state = create_copy(state)
    for i in range(Y):
        for j in range(X):
            nb = count_neighbours(state, i, j)
            #if nb != 0:
            #    print j, i, nb
            if nb > 3 or nb < 2:
                new_state = set(new_state, [[i, j]], 0)
            elif nb == 3:
                new_state = set(new_state, [[i, j]], 1)
            else:
                new_state = set(new_state, [[i, j]], get(state, i, j))
    return new_state

def count_neighbours(state, y, x):
    pos = [[x-1,y-1],[x,y-1],[x+1,y-1],[x+1,y],[x+1,y+1],[x,y+1],[x-1,y+1],[x-1,y]]
    count = 0
    for p in pos:
        count = count + get(state, p[1], p[0]) 
    return count

def print_state(state):
    for i in range(Y):
        for j in range(X):
           print state[i][j],
        print
    print

def test_state_machine ():
    print create_empty_state() == create_empty_state()
    print create_empty_state() == create_copy(create_empty_state()) 
    a = create_empty_state()
    a[2][3] = 1
    a[3][4] = 1
    b = create_copy(a)
    print b == a
    b = create_empty_state()
    b = set(b, [[2, 3], [3, 4]], 1)
    print b == a
    b = set(b, [[4, 8]], 1)
    print not(b == a)
    a = set(a, [[2, 5]], 1)
    print a == set(a, [[-1, 0], [9, 11]], 1)
    a = set(create_empty_state(), [[1, 1], [1, 2], [1, 3]], 1)
    a1 = get_next_state(a)
    a2 = get_next_state(a1)
    print not(a == a1)
    print a2 == a

def test():
    test_state_machine()

#test()
