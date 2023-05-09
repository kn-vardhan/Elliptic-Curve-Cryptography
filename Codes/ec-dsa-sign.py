# import all functions from ecc_func.py
from ecc_func import *

# load necessary libraries for SHA-2
import hashlib
import secrets


# public key setup
def public_key_setup(G, p, a, b):
    
    # Define private key
    # Choose a random integer k, 1 < k < p-1
    d = secrets.randbelow(exclusive_upper_bound=p-1) + 1

    # Generate public key Q = dG
    Q = ec_mult(d, G, p, a, b)

    # The public key Q can be sent to the recipient
    return Q, d


# generate hash using SHA-2
def generate_hash(message):
    # encode the message
    message = message.encode('utf-8')

    # generate hash using SHA-2
    hash = hashlib.sha256(message).hexdigest()

    # convert hash to integer
    hash = int(hash, 16)

    return hash


# sign the message
def sign(G, M, p, a, b):

    # get public key Q
    Q, d = public_key_setup(G, p, a, b)

    # Ln - bit length of the curve order n
    Ln = len(bin(p)[2:])

    # z - Ln leftmost bits of hash(M)
    z = generate_hash(M) >> (256 - Ln)

    while True:
        # Define private key
        # Choose a random integer k, 1 < k < n-1
        k = secrets.randbelow(exclusive_upper_bound=p-1) + 1

        # Find curve point
        # (x1, y1) = kG
        kG = ec_mult(k, G, p, a, b)

        # r = x1 mod n
        r = kG.x % (p)

        # s = (z + rd) / k mod n
        s = ((z + r*d) * pow(k, -1, p)) % (p)

        # if r != 0 and s != 0, then the signature is valid
        if r != 0 and s != 0:
            break
    
    # The signature (r, s) can be sent to the recipient
    # (r, -s mod n) is also a valid signature
    return r, s, Q, d


# main program
if __name__ == '__main__':
    print("Curve E: y^2 = x^3 + ax + b (mod p)")

    # get the curve parameters
    p = 7559
    a = 0
    b = 7

    # get generator G
    G = Point(12, 217)

    # get message M as input
    M = input("Enter message: ")

    # sign the message
    r, s, Q, d = sign(G, M, p, a, b)

    # print the signature
    print(f'Signature: ({r}, {s})')

    # print the public key
    print(f'Public key: ({Q.x}, {Q.y})')
