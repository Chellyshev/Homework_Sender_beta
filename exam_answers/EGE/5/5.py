for N in range(1, 1000):
    N_2 = bin(N)[2:]
    if N % 2 == 0:
        N_2 += '0'
    else:
        N_2 += '1'
    if N_2.count('1') % 3 == 0:
        N_2 = '11' + N_2[2:]
    else:
        N_2 = '10' + N_2[2:]
    R = int(N_2, 2)
    if R >= 26:
        print(N)
        break