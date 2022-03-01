"""

 * Advanced Encryption Standard
 * Finite Field operation
 * Subbytes(inverse of multiplication, affine transformation)
 * MixColumns(xtime)
 * Based on the document FIPS PUB 197
 * @2022.02.28
 
"""

# Addition in GF(2^8)
def gadd(a, b):
    return a^b

# Subtraction in GF(2^8)
def gsub(a, b):
    return a^b

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

# Multiplicative inverse
def mul_inverse(a):
    if a == 0:
        return 0
    for i in range(1, 256):
        if aes_gmult(a, i) == 1:
            return i

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

# Addition of 4 byte words
def coef_add(a, b):
    d = list(range(4))
    d[0] = a[0]^b[0]
    d[1] = a[1]^b[1]
    d[2] = a[2]^b[2]
    d[3] = a[3]^b[3]
    return d
    
# Multiplication of 4 byte words
def coef_mult(a, b, d):
    d[0] = aes_gmult(a[0],b[0])^aes_gmult(a[3],b[1])^aes_gmult(a[2],b[2])^aes_gmult(a[1],b[3])
    d[1] = aes_gmult(a[1],b[0])^aes_gmult(a[0],b[1])^aes_gmult(a[3],b[2])^aes_gmult(a[2],b[3])
    d[2] = aes_gmult(a[2],b[0])^aes_gmult(a[1],b[1])^aes_gmult(a[0],b[2])^aes_gmult(a[3],b[3])
    d[3] = aes_gmult(a[3],b[0])^aes_gmult(a[2],b[1])^aes_gmult(a[1],b[2])^aes_gmult(a[0],b[3])
    return d
 
K = 0
Nb = 4
Nk = 0
Nr = 0

def aes_init(size):
    global Nk
    global Nr
    if size == 16:    
        Nk = 4
        Nr = 10
    elif size == 24:
        Nk = 6
        Nr = 12
    else:                       #size == 32
        Nk = 8
        Nr = 14
    return Nb*(Nr+1)*4

R = [0x02, 0x00, 0x00, 0x00]

def Rcon(i):
    global R
    if i == 1:
        R[0] = 0x01         # x^(1-1) = x^0 = 1
    elif i > 1:
        R[0] = 0x02
        i -= 1
        while i>1:
            R[0] = aes_gmult(R[0], 0x02)
            i -= 1
    return R

def add_round_key(state, w, r):
    for c in range(Nb):
        state[Nb*0+c] = state[Nb*0+c]^w[4*Nb*r+4*c+0]   
        state[Nb*1+c] = state[Nb*1+c]^w[4*Nb*r+4*c+1]
        state[Nb*2+c] = state[Nb*2+c]^w[4*Nb*r+4*c+2]
        state[Nb*3+c] = state[Nb*3+c]^w[4*Nb*r+4*c+3]
    return state

def mix_columns(state):
    a = [0x02, 0x01, 0x01, 0x03]
    col = list(range(4))
    res = list(range(4))
    
    for j in range(Nb):
        for i in range(4):
            col[i] = state[Nb*i+j]
            
        coef_mult(a, col, res)
        
        for i in range(4):
            state[Nb*i+j] = res[i]
    
    return state

def inv_mix_columns(state):
    a = [0x0e, 0x09, 0x0d, 0x0b]
    col = list(range(4))
    res = list(range(4))
    
    for j in range(Nb):
        for i in range(4):
            col[i] = state[Nb*i+j]
            
        coef_mult(a, col, res)
        
        for i in range(4):
            state[Nb*i+j] = res[i]
    
    return state
            
def shift_rows(state):
    for i in range(1, 4):
        s = 0
        while s < i:
            tmp = state[Nb*i+0]
            
            for k in range(1, Nb):
                state[Nb*i+k-1] = state[Nb*i+k]
            
            state[Nb*i+Nb-1] = tmp
            s += 1
    
    return state

def inv_shift_rows(state):
    for i in range(1, 4):
        s = 0
        while s < i:
            tmp = state[Nb*i+Nb-1]
            
            for k in range(Nb-1, 0, -1):
                state[Nb*i+k] = state[Nb*i+k-1]
            
            state[Nb*i+0] = tmp
            s += 1
    
    return state

def sub_bytes(state):
    for i in range(4):
        for j in range(Nb):
            state[Nb*i+j] = affine_trans(mul_inverse(state[Nb*i+j]))
    return state


def inv_sub_bytes(state):
    for i in range(4):
        for j in range(Nb):
            state[Nb*i+j] = mul_inverse(inv_affine_trans(state[Nb*i+j]))
    return state

def sub_word(w):
    for i in range(4):
        w[i] = affine_trans(mul_inverse(w[i]))
    return w

def rot_word(w):
    tmp = w[0]
    
    for i in range(3):
        w[i] = w[i+1]
        
    w[3] = tmp
    
    return w

def aes_key_expansion(key, w):
    tmp = list(range(4))
    k_len = Nb*(Nr+1)
    
    for i in range(Nk):
        w[4*i+0] = key[4*i+0]
        w[4*i+1] = key[4*i+1]
        w[4*i+2] = key[4*i+2]
        w[4*i+3] = key[4*i+3]
    for i in range(Nk, k_len):
        tmp[0] = w[4*(i-1)+0]
        tmp[1] = w[4*(i-1)+1]
        tmp[2] = w[4*(i-1)+2]
        tmp[3] = w[4*(i-1)+3]
        
        if (i%Nk == 0):
            tmp = rot_word(tmp)
            tmp = sub_word(tmp)
            tmp = coef_add(tmp, Rcon(i/Nk))
        elif((Nk>6)and(i%Nk==4)):
            tmp = sub_word(tmp)
            
        w[4*i+0] = w[4*(i-Nk)+0]^tmp[0]
        w[4*i+1] = w[4*(i-Nk)+1]^tmp[1]
        w[4*i+2] = w[4*(i-Nk)+2]^tmp[2]
        w[4*i+3] = w[4*(i-Nk)+3]^tmp[3]    
      
    return w

def aes_cipher(input, output, w):
    state = list(range(4*Nb))
    
    for i in range(4):
        for j in range(Nb):
            state[Nb*i+j] = input[i+4*j]
    
    state = add_round_key(state, w, 0)
    
    for r in range(1, Nr):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, w, r)

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, w, Nr)

    for i in range(4):
        for j in range(Nb):
            output[i+4*j] = state[Nb*i+j]
    
    return output

def aes_inv_cipher(input, output, w):
    state = list(range(4*Nb))
    
    for i in range(4):
        for j in range(Nb):
            state[Nb*i+j] = input[i+4*j]
            
    state = add_round_key(state, w, Nr)
    
    for r in range(Nr-1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, w, r)
        state = inv_mix_columns(state)
        
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, w, 0)
    
    for i in range(4):
        for j in range(Nb):
            output[i+4*j] = state[Nb*i+j]
    return output

# main
	 
# 128 bits 

key = [
    0x2b, 0x7e, 0x15, 0x16,
    0x28, 0xae, 0xd2, 0xa6,
    0xab, 0xf7, 0x15, 0x88,
    0x09, 0xcf, 0x4f, 0x3c]

aes_in = [
    0x32, 0x43, 0xf6, 0xa8,
    0x88, 0x5a, 0x30, 0x8d,
    0x31, 0x31, 0x98, 0xa2,
    0xe0, 0x37, 0x07, 0x34]    # 128


aes_out = list(range(16)) 

aes_init(len(key))
w = list(range(Nb*(Nr+1)*4))
w = aes_key_expansion(key, w)

print("Plaintest message: ")
for i in range(4):
    print("{0:02x} {1:02x} {2:02x} {3:02x}".format(aes_in[4*i+0], aes_in[4*i+1], aes_in[4*i+2], aes_in[4*i+3]), end=' ')
print('\n')

aes_out = aes_cipher(aes_in, aes_out, w)

print("Ciphered message: ")
for i in range(4):
    print("{0:02x} {1:02x} {2:02x} {3:02x}".format(aes_out[4*i+0], aes_out[4*i+1], aes_out[4*i+2], aes_out[4*i+3]), end=' ')
print('\n')

aes_in = aes_inv_cipher(aes_out, aes_in, w)

print("Original message (after inv cipher): ")
for i in range(4):
    print("{0:02x} {1:02x} {2:02x} {3:02x}".format(aes_in[4*i+0], aes_in[4*i+1], aes_in[4*i+2], aes_in[4*i+3]), end=' ')
print('\n')
