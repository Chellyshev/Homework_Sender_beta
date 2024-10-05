def translator(n, cc):
    n_cc = ''
    while n > 0:
        n_cc += str(n % cc)
        n //= cc
    return n_cc[::-1]

for N in range(1000, 0, -1):
    N_4 = translator(N, 4)
    if N % 4 == 0:
        N_4 += N_4[-2:]
    else:
        N_4 += translator((N % 4) * 2, 4)
    R = int(N_4, 4)
    if R < 369:
        print(N)
        break