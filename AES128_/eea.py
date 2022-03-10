# Multiplication Polynomial
def mul_polynomial(a, b):
    if a == 0 or b == 0:
        return 0
    c = 0

    while a != 0:
        if a & 1 == 1:
            c ^= b 

        b <<= 1
        a >>= 1
        
    return c

def bit_len(a):
    if a == 0:
        return 1
    b = 0
    while a != 0:
        b += 1
        a >>= 1
    return b

# q = a/b, r = a%b
def qr(b, a):
    bit_b = bit_len(b)
    bit_a = bit_len(a)
    q = [0 for _ in range(bit_b - bit_a + 1)]

    while True:
        tmp_a = a
        bit_b = bit_len(b)
        q[bit_b-bit_a] =  1
        if bit_b < bit_a:
            break
        tmp_a <<= bit_b - bit_a
        b ^= tmp_a
        r = b
    q = ''.join(map(str, q[::-1]))

    return [int(q, 2), r]


def mul_inverse(a, m):
    x = []
    t = m
    v = a
    cnt = 0

    while True:
        q_r = qr(t, v)
        q = q_r[0]
        r = q_r[1]
        
        x.append([t, v, -q, r])
        
        if r == 1:
            break

        t = v
        v = r
        cnt += 1
    print(x)

    coef = [x[-1][2], 1]
    print(coef)
    if cnt == 0:
        return q

    for i in range(cnt-1, -1, -1):
        print()
        print(i)
        
        si_1 = 1
        si_2 = 1

        tmp = coef[0]
        if coef[0] < 0 :
            si_1 = -1
            coef[0] *= -1
        if x[i][2] < 0 :
            si_2 = -1
            x[i][2] *= -1
        print(coef)
        print(x[i][2])
        print(coef[1])
        print((si_1*si_2) * mul_polynomial(coef[0],(x[i][2])))
        coef[0] = coef[1] ^ ((si_1*si_2) * mul_polynomial(coef[0],(x[i][2])))
        coef[1] = tmp
    
    print(coef)

    #if coef[0] < 0:
    #    print(m^coef[0])
    #    return m^coef[0]
        
    return coef[0]

print(hex(mul_inverse(0x41, 283)))
    

