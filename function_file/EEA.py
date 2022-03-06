def EEA_iterative(x, y):
    t = [x, y]
    u = [1, 0]
    v = [0, 1]

    while t[1] != 0:
        q = int(t[0] / t[1])
        r = t[0] % t[1]
        t[0] = t[1]
        t[1] = r
        tmp_u = u[0] - (q*u[1])
        tmp_v = v[0] - (q*v[1])
        u[0] = u[1]
        v[0] = v[1]
        u[1] = tmp_u
        v[1] = tmp_v

    tuv = [t[0], u[0], v[0]]
    return tuv

def EEA_recursive(a, b):
    rec = [a, 1, 0]
    if b == 0:
        return rec
    else:
        rec = EEA_recursive(b, a%b)
        rec = [rec[0], rec[2], rec[1] - (a//b)*rec[2]]
    return rec

a = 698
b = 638

print(EEA_iterative(a, b))
print(EEA_recursive(a, b))
