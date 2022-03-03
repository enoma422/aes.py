'''

 def affine_trans(x)
 1. matrix form
 2. over GF(2) : b_i'
 
'''

# 1. matrix form
# Affine Transformation
def affine_trans(a):
    affine = [0b11111000, 0b01111100, 0b00111110, 0b00011111, 0b10001111, 0b11000111, 0b11100011, 0b11110001]
    b = ''

    for i in range(8):
        b += str(bin(a&affine[i]).count('1') % 2)
    
    b = int(b, 2) ^ int('01100011', 2)

    return b

# Inverse of the Affine Transformation
def inv_affine_trans(a):
    inv_affine = [0b01010010, 0b00101001, 0b10010100, 0b01001010, 0b00100101, 0b10010010, 0b01001001, 0b10100100]
    b = ''

    for i in range(8):
        b += str(bin(a&inv_affine[i]).count('1') % 2)

    b = int(b, 2) ^ int('00000101', 2)

    return b


# 2. over GF(2) : b_i'
# Affine Transformation over GF(2) : b_i'
def affine_trans(x):
    # byte c with value {0x63} or {0b01100011}
    c = 0b01100011
    b_num = [0 for _ in range(5)]
    res = [0 for _ in range(8)]
    
    for i in range(8):
        a = x
        # b_i' = b_i + b_(i+4)mod8 + b_(i+5)mod8 + b_(i+6)mod8 + b_(i+7)mod8 + c_i
        b_num[0] = i % 8
        b_num[1] = (i+4) % 8
        b_num[2] = (i+5) % 8
        b_num[3] = (i+6) % 8
        b_num[4] = (i+7) % 8
        b_num.sort()

        a >>= b_num[0]
        res[i] ^= a&1
        
        for j in range(4):
            a >>= b_num[j+1] - b_num[j]
            res[i] ^= a&1
            
        res[i] ^= c&1
        c >>= 1
        
    res = ''.join(map(str, res[::-1]))
    
    return int(res, 2)

# Inverse of the Affine Transformation over GF(2) : b_i'
def inv_affine_trans(x):
    # byte c with value {0x05} or {0b00000101}
    c = 0b00000101
    b_num = [0 for _ in range(3)]
    res = [0 for _ in range(8)]
    
    for i in range(8):
        a = x
        # b_i' = b_(i+2)mod8 + b_(i+5)mod8 + b_(i+7)mod8 + c_i
        b_num[0] = (i+2) % 8
        b_num[1] = (i+5) % 8
        b_num[2] = (i+7) % 8
        b_num.sort()

        a >>= b_num[0]
        res[i] ^= a&1
        
        for j in range(2):
            a >>= b_num[j+1] - b_num[j]
            res[i] ^= a&1

        res[i] ^= c&1
        c >>= 1
    res = ''.join(map(str, res[::-1]))

    return int(res, 2)