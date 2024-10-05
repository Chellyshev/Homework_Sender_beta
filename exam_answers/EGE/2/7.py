print('x y z w F')
for x in range(2):
    for y in range(2):
        for z in range(2):
            for w in range(2):
                F = not(y <= (not(z <= w))) and ((not z) <= (not w == x))
                print(x, y, z, w, int(F))