# Multiplication Polynomial
from codecs import utf_16_be_decode
from unicodedata import ucd_3_2_0
# Addition in GF(2^8)
def gadd(a, b):
    return a^b


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

# q = a/b, r = a%b (a>b)
def qr(a, b):
 #   print("a= {}".format(a))
#    print("b= {}".format(b))
    
    
    bit_b = bit_len(b)
    bit_a = bit_len(a)
    
    if bit_a < bit_b:
        return [0, a]
    
    q = [0 for _ in range(bit_a - bit_b + 1)]
    print("q= {}".format(q))

    while True:
        tmp_b =b
        bit_a= bit_len(a)
        q[bit_a-bit_b] ^=  1
       # print("q= {}".format(q))
       # print("bita= {}".format(bit_a))
       # print("bitb= {}".format(bit_b))
       # print("tmpb= {}".format(tmp_b))

        tmp_b <<= (bit_a - bit_b)
      #  print("tmpab= {}".format(tmp_b))

        a ^= tmp_b
      #  print("a= {}".format(a))

        if bit_len(a) <bit_len(b):
            break
      #  print("bita= {}".format(bit_a))

    r = a
    q = ''.join(map(str, q[::-1]))

    return [int(q, 2), r]

#print("qr= {}".format(qr(4,5)))


def mul_inverse(a, m):    # 확장 유클리드 알고리듬. a의 mod m상의 역원찾기      
    u0=1
    u1=0
    t0=a
    t1=m

    while t1!=0 and t1!=1:
        t2 = t0
        t0 = t1
       # print("11t2= {}".format(t2))
       # print("11t1= {}".format(t0))

        q_r = qr(t2, t1)
        q = q_r[0]
        t1 = q_r[1]
        
       # print("11q= {}".format(q))
       # print("11r= {}".format(t1))
        
        u2 = u0
        u0 = u1
        u1 = mod_polynomial((u2 ^ mul_polynomial(q, u1)), m)
       # print("u00000= {}".format(u0))
       # print("u11111= {}".format(u1))
       # print("u22222= {}".format(u2)) 
       # print("11t2= {}".format(t2))
       # print("11t1= {}".format(t1))

       # print("11q= {}".format(q))
       # print("11r= {}".format(t1))
       # print("==================")


    return u1

a=0x3
m=283    ##m은 기약으로로 넣어야 편함.  # 283 = x8+x4+x3+x+1

d=(mul_inverse(a,m))
print(hex(d))
print(hex(mod_polynomial(mul_polynomial(d, a), m)))



'''

1001

101

               100
10010 |   01000001
           10010     
              1001
01001000
01000001
10010000
11001010
11001000
00110010

'''
