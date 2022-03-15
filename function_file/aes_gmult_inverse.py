'''

 def aes_gmult(a, b)
 1. polynomial mod m(x)
 2. xtime
 
 def mul_inverse(a)
 1. for i in range(1, 256): aes_gmult(a, i) = 1
 2. Extended Euclidean Algorithm
 
'''

# Addition in GF(2^8)
def gadd(a, b):
    return a^b

# Subtraction in GF(2^8)
def gsub(a, b):
    return a^b

# 1. polynomial mod m(x)
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

# Modulo an irreducible polynomial
def mod_polynomial(a, m):
    bit_m = m.bit_length()
    while True:
        bit_a = a.bit_length()
        if bit_a < bit_m:
            break
        mshift = m << (bit_a - bit_m)
        a ^= mshift
    return a
    
# Multiplication in Gf(2^8)
def aes_gmult(a, b):
    # m(x) = x^8 + x^4 + x^3 + x + 1 
    # m = (100011011)_2
    return mod_polynomial(mul_polynomial(a, b), 0b100011011)


# 2. xtime
# xtime(f(x)) = x * f(x)
def xtime(a):
    b = (a >> 7) & 0x01
    if b == 1:
        res = (a << 1) ^ 0x1b
    else:
        res = a << 1
    return res & 0xff

# Multiplication in Gf(2^8)
def aes_gmult(a, b):
    d = 0x00
    
    for i in range(7, -1, -1):
        coef = (a >> i) & 1
        d = xtime(d)
        
        if coef == 1:
            d = gadd(d, b)
            
    return d


# 1. for i in range(1, 256): aes_gmult(a, i) = 1
# Multiplicative inverse
def mul_inverse(a):
    if a == 0:
        return 0
    for i in range(1, 256):
        if aes_gmult(a, i) == 1:
            return i
      
        
# 2. Extended Euclidean Algorithm
# q = a/b, r = a%b (a>b)
def qr(a, b):
    bit_b = b.bit_length()
    bit_a = a.bit_length()
    
    if bit_a < bit_b:
        return [0, a]
    
    q = [0 for _ in range(bit_a - bit_b + 1)]=

    while True:
        tmp_b = b
        bit_a = a.bit_length()
        q[bit_a - bit_b] ^=  1

        tmp_b <<= (bit_a - bit_b)

        a ^= tmp_b

        if a.bit_length() < b.bit_length():
            break

    r = a
    q = ''.join(map(str, q[::-1]))

    return [int(q, 2), r]

# Multiplicative inverse
def mul_inverse(a): 
    m = 283
    if a == 0:
        return 0    
    u0 = 1
    u1 = 0
    t0 = a
    t1 = m

    while t1!=0 and t1!=1:
        t2 = t0
        t0 = t1

        q_r = qr(t2, t1)
        q = q_r[0]
        t1 = q_r[1]
        
        u2 = u0
        u0 = u1
        u1 = mod_polynomial((u2 ^ mul_polynomial(q, u1)), m)

    return u1
