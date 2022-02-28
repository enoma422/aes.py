
def mul_polynomial(x, y):
    if x == 0 or y == 0:
        return 0
    z = 0

    while x != 0:
        #x의 제일 마지막 비트가 1이면 addition(XOR)
        if x & 1 == 1:
            z ^= y 

        y <<= 1
        x >>= 1
        
    return z

def bit_len(x):
    return (len(bin(x))-2)

def mod_polynomial(x, m):
    bit_m = bit_len(m)
    while True:
        bit_x = bit_len(x)
        if bit_x < bit_m:
            break
        mshift = m << (bit_x - bit_m)
        x ^= mshift
    return x
    
def aes_gmult(x, y):
    # m(x) = x^8 + x^4 + x^3 + x + 1 
    # m = (100011011)_2 = (283)_10
    return mod_polynomial(mul_polynomial(x, y), 283)

def mul_inverse(x):
    if x == 0:
        return 0
    for i in range(1, 256):
        if aes_gmult(x, i) == 1:
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

def sub_bytes(x):
    return affine_trans(mul_inverse(x))

def inv_sub_bytes(x):
    return mul_inverse(inv_affine_trans(x))


print(mul_polynomial(33, 27))

print(bit_len(142))

print(mod_polynomial(10710, 283))
print(aes_gmult(20, 153))    

print(hex(mul_inverse(0x02)))
print(hex(affine_trans(0x8d)))

print(hex(sub_bytes(0xc4)))
print(hex(inv_sub_bytes(0x1c)))