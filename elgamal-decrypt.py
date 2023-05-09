# import all functions from the ecc_func.py
from ecc_func import *


# ElGamal decryption
def decryption(C1, C2, d, p, a, b):

    # Compute the plaintext M = C2 - dC1
    dC1 = ec_mult(d, C1, p, a, b)
    dC1 = Point(dC1.x, -dC1.y % p)
    M = ec_add(C2, dC1, p, a, b)

    # The plaintext M can be sent to the recipient
    return M


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

    # get the ciphertext
    C1, C2 = get_ciphertext()

    # get the private key
    d = get_private_key()

    # decrypt the ciphertext
    P = decryption(C1, C2, d, p, a, b)

    # print the plaintext
    print(f'Plaintext: ({P.x}, {P.y})')

    # The plaintext P = (3085, 2919) is the original message
