# aes.py

* https://github.com/dhuertas/AES 를 참고하여 python으로 구현하였습니다.
* FIPS 197, Advanced Encryption Standard (AES) 를 참고하여 공부했습니다.

Plaintest message: 
32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34 

Ciphered message:
39 25 84 1d 02 dc 09 fb dc 11 85 97 19 6a 0b 32

Original message (after inv cipher):
32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34


# AES128_ - over_GF.py
 def aes_gmult(a, b) - xtime
 def mul_inverse(a) - for i in range(1, 256): aes_gmult(a, i) = 1
 def affine_trans(x) - over GF(2) : b_i'
 def mix_columns(state) - xtime
 
# AES128_ - EEA_matrix.py
 def aes_gmult(a, b) - polynomial mod m(x)
 def mul_inverse(a) - Extended Euclidean Algorithm
 def affine_trans(x) - matrix form
 def mix_columns(state) - matrix form


# function file - aes_gmult_inverse.py
 def aes_gmult(a, b)
 1. polynomial mod m(x)
 2. xtime
 def mul_inverse(a)
 1. for i in range(1, 256): aes_gmult(a, i) = 1
 2. Extended Euclidean Algorithm
 
# function file - affine_trans.py
  def affine_trans(x)
 1. matrix form
 2. over GF(2) : b_i'

# function file - mix_columns.py
 def mix_columns(state)
 1. matrix form
 2. xtime
