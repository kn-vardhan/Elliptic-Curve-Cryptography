# import all functions from ecc_func.py
from ecc_func import *


# public key setup
def public_key_setup(G, p, a, b):
    
    # Define private key
    # Choose a random integer k, 1 < k < p-1
    d = secrets.randbelow(exclusive_upper_bound=p-1) + 1

    # Generate public key Q = dG
    Q = ec_mult(d, G, p, a, b)

    # The public key Q can be sent to the recipient
    return Q, d


# ElGamal encryption
def encryption(G, M, p, a, b):
    
    # get public key Q
    Q, d = public_key_setup(G, p, a, b)

    # Define private key
    # Choose a random integer k, 1 < k < p-1
    k = secrets.randbelow(exclusive_upper_bound=p-1) + 1

    # Compute the ciphertext (C1, C2)
    # C1 = kG
    C1 = ec_mult(k, G, p, a, b)

    # C2 = M + kQ
    kQ = ec_mult(k, Q, p, a, b)
    C2 = ec_add(M, kQ, p, a, b)

    # The ciphertext (C1, C2) can be sent to the recipient
    return C1, C2, d


# main program
if __name__ == '__main__':
    print("Curve E: y^2 = x^3 + ax + b (mod p)")

    # get the curve parameters
    p = 7559
    a = 0
    b = 7

    # get generator G
    G = Point(12, 217)

    # get the message M as a point on the curve
    M = Point(3085, 2919)

    # encrypt the message
    C1, C2, d = encryption(G, M, p, a, b)

    # print the ciphertext
    print(f'Ciphertext: ({C1.x}, {C1.y}), ({C2.x}, {C2.y})')

    # print the private key
    print(f'Private Key d = {d}')
