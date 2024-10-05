for N in range(1, 1000):
    N_2 = bin(N)[2:]
    if len(N_2) % 2 == 0:
        N_2 = N_2[0:len(N_2) // 2] + '1' + N_2[len(N_2) // 2:]
    R = int(N_2, 2)
    if R >= 26:
        print(N)
        break