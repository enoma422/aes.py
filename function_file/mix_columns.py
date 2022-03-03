'''

 def mix_columns(state)
 1. matrix form
 2. xtime
 
'''

# 1. matrix form
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


# 2. xtime
def mix_columns(state):
    col = list(range(4))
    res = list(range(4))
    
    for j in range(Nb):
        for i in range(4):
            col[i] = state[Nb*i+j]
            
        res[0] = xtime(col[0]) ^ (xtime(col[1])^col[1]) ^ col[2] ^ col[3]
        res[1] = col[0] ^ xtime(col[1]) ^ (xtime(col[2])^col[2]) ^ col[3]
        res[2] = col[0] ^ col[1] ^ xtime(col[2]) ^ (xtime(col[3])^col[3])
        res[3] = (xtime(col[0])^col[0]) ^ col[1] ^ col[2] ^ xtime(col[3])
        
        for i in range(4):
            state[Nb*i+j] = res[i]
            
    return state

def inv_mix_columns(state):
    col = list(range(4))
    res = list(range(4))
    
    for j in range(Nb):
        for i in range(4):
            col[i] = state[Nb*i+j]
            
        res[0] = (xtime(xtime(xtime(col[0])))^xtime(xtime(col[0]))^xtime(col[0])) ^ (xtime(xtime(xtime(col[1])))^xtime(col[1])^col[1]) ^ (xtime(xtime(xtime(col[2])))^xtime(xtime(col[2]))^col[2]) ^ (xtime(xtime(xtime(col[3])))^col[3])
        res[1] = (xtime(xtime(xtime(col[0])))^col[0]) ^ (xtime(xtime(xtime(col[1])))^xtime(xtime(col[1]))^xtime(col[1])) ^ (xtime(xtime(xtime(col[2])))^xtime(col[2])^col[2]) ^ (xtime(xtime(xtime(col[3])))^xtime(xtime(col[3]))^col[3])
        res[2] = (xtime(xtime(xtime(col[0])))^xtime(xtime(col[0]))^col[0]) ^ (xtime(xtime(xtime(col[1])))^col[1]) ^ (xtime(xtime(xtime(col[2])))^xtime(xtime(col[2]))^xtime(col[2])) ^ (xtime(xtime(xtime(col[3])))^xtime(col[3])^col[3])
        res[3] = (xtime(xtime(xtime(col[0])))^xtime(col[0])^col[0]) ^ (xtime(xtime(xtime(col[1])))^xtime(xtime(col[1]))^col[1]) ^ (xtime(xtime(xtime(col[2])))^col[2]) ^ (xtime(xtime(xtime(col[3])))^xtime(xtime(col[3]))^xtime(col[3]))
        
        for i in range(4):
            state[Nb*i+j] = res[i]
    
    return state

# ------------------------------------------

Nb = 4

# Multiplication of 4 byte words
def coef_mult(a, b, d):
    d[0] = aes_gmult(a[0],b[0])^aes_gmult(a[3],b[1])^aes_gmult(a[2],b[2])^aes_gmult(a[1],b[3])
    d[1] = aes_gmult(a[1],b[0])^aes_gmult(a[0],b[1])^aes_gmult(a[3],b[2])^aes_gmult(a[2],b[3])
    d[2] = aes_gmult(a[2],b[0])^aes_gmult(a[1],b[1])^aes_gmult(a[0],b[2])^aes_gmult(a[3],b[3])
    d[3] = aes_gmult(a[3],b[0])^aes_gmult(a[2],b[1])^aes_gmult(a[1],b[2])^aes_gmult(a[0],b[3])
    return d

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

# Addition in GF(2^8)
def gadd(a, b):
    return a^b