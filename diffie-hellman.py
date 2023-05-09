# import all functions from ecc_func.py
from ecc_func import *


# Diffie-Hellman key exchange
def key_exchange(G, p, a, b):
    
    # Define private key from Alice
    # Choose a random integer k, 1 < k < 100
    a = random.randint(1, 100)

    # Define private key from Bob
    # Choose a random integer k, 1 < k < 100
    b = random.randint(1, 100)

    while a == b:
        b = random.randint(1, 100)

    # Compute the public key A = aG
    A = ec_mult(a, G, p, a, b)

    # Compute the public key B = bG
    B = ec_mult(b, G, p, a, b)

    # Compute the shared secret key K = aB = bA
    K1 = ec_mult(a, B, p, a, b)
    K2 = ec_mult(b, A, p, a, b)

    # The shared secret key K can be used as the key for a symmetric cipher
    return K1, K2


# main program
if __name__ == '__main__':
    print("Curve E: y^2 = x^3 + ax + b (mod p)")

    # get the curve parameters
    p = 7559
    a = 0
    b = 7

    # get generator G
    G = Point(12, 217)

    # Alice and Bob perform key exchange
    K1, K2 = key_exchange(G, p, a, b)

    # print the shared secret key
    print(K1, K2)
