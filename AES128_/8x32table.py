
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

# Multiplicative inverse
def mul_inverse(a):
    if a == 0:
        return 0
    for i in range(1, 256):
        if aes_gmult(a, i) == 1:
            return i

def affine_trans(x):
    affine = [248, 124, 62, 31, 143, 199, 227, 241]
    y = ''

    for i in range(8):
        y += str(bin(x&affine[i]).count('1') % 2)
    
    y = int(y, 2) ^ int('01100011', 2)

    return y

def inv_affine_trans(x):
    inv_affine = [82, 41, 148, 74, 37, 146, 73, 164]
    y = ''

    for i in range(8):
        y += str(bin(x&inv_affine[i]).count('1') % 2)

    y = int(y, 2) ^ int('00000101', 2)

    return y

def s_box(x):
    return affine_trans(mul_inverse(x))

def T_e0():
    res = []
    for i in range(256):
        res.append((((aes_gmult(0x02, s_box(i)) << 24) ^ ((s_box(i) << 16)) ^ ((s_box(i) << 8)) ^ ((aes_gmult(0x03,s_box(i)))))))
    return res

def T_shift(table):
    for i in range(256):
        tmp = (table[i] & 0xff)
        table[i] = ((table[i] >> 8) & 0x00ffffff) ^ (tmp << 24)
    return table

# Te0 : shift

# s_box_table(Te0)로 고정
def s_box_table(table):
    for i in range(256):
        table[i] = (table[i] >> 8) & 0xff
    return table

Te0 = T_e0()
#Te1 = T_shift(Te0)
#Te2 = T_shift(Te1)
#Te3 = T_shift(Te2)

#ttable = s_box_table(Te0)

for i in range(256):
    if i % 4 == 0:
        print()
    print(hex(Te0[i]), end=' ')
