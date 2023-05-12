"""
This file implements the functions we defined in ecc_dlp.py
It finds k for which kP = Q, where P and Q are points on the elliptic curve
"""

import sys

sys.path.append("C:/Users/Anita Dash/Downloads")

import ecc_func as ecc
import ecc_dlp as dlp

a = 1
b = 44
p = 229
N = 239
A = ecc.Point(5, 116)
B = ecc.Point(155, 166)

print("Given elliptic curve is: y^2 = x^3 +", a, "x +", b, "mod", p)
print("Generator point is: ", A)
print("Given point is: ", B)
print("Order of the point", A, "is:", dlp.order_point(A, p, a, b))
print("Baby step Giant step method: k value is: ", dlp.BG(A, B, p, a, b))
for i in range(100):
    k = dlp.pollard(A, B, p, a, b)
    if ecc.ec_mult(k, A, p, a, b) == B:
        print("Pollard's rho method: k value is: ", k)
        break
print("Pohlig-Hellman method: k value is: ", dlp.Pohlig(A, B, N, p, a, b))
