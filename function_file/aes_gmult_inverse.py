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

def bit_len(a):
    if a == 0:
        return 1
    b = 0
    while a != 0:
        b += 1
        a >>= 1
    return b

# Modulo an irreducible polynomial
def mod_polynomial(a, m):
    bit_m = bit_len(m)
    while True:
        bit_a = bit_len(a)
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
    return res % 0x100

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
 