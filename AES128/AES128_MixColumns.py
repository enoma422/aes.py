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

def mix_columns(state):
    Nb = 4
    a = [0x02, 0x01, 0x01, 0x03]
    col = list(range(4))
    res = list(range(4))
    
    for j in range(Nb):
        for i in range(4):
            col[i] = state[Nb*i+j]
            
        mul_polynomial(a, col, res)
        
        for i in range(4):
            state[Nb*i+j] = res[i]
    
    return state

print(mix_columns([0x01, 0x00, 0x00, 0x01]))