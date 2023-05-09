# import all functions from ecc_func.py
from ecc_func import *

# load necessary libraries for SHA-2
import hashlib
import secrets


# verify public key
def verify_public_key(Q, p, a, b):
    # check if Q is a valid point on the curve
    # then check if Q is a generator

    flag1 = valid(Q, p, a, b)
    flag2 = True if ec_mult(p+1, Q, p, a, b) == O else False

    return flag1 and flag2


# generate hash using SHA-2
def generate_hash(message):
    # encode the message
    message = message.encode('utf-8')

    # generate hash using SHA-2
    hash = hashlib.sha256(message).hexdigest()

    # convert hash to integer
    hash = int(hash, 16)

    return hash


# verify signature
def verify(G, Q, M, r, s, p, a, b):

    # verify if r and s are in the range [1, n-1]
    if r < 1 or r > p-1 or s < 1 or s > p-1:
        return False
    
    # calculate hash of the message
    hash = generate_hash(M)

    # Ln - bit length of the curve order n
    Ln = len(bin(p)[2:])

    # z - Ln leftmost bits of hash(M)
    z = hash >> (256 - Ln)

    # u1 = zs^-1 mod n
    s_inv = pow(s, -1, p)
    u1 = (z * s_inv) % (p)

    # u2 = rs^-1 mod n
    u2 = (r * s_inv) % (p)

    # Find curve point
    # (x1, y1) = u1G + u2Q
    u1G = ec_mult(u1, G, p, a, b)
    u2Q = ec_mult(u2, Q, p, a, b)
    u1G_u2Q = ec_add(u1G, u2Q, p, a, b)

    # verify point
    if u1G_u2Q == O:
        return False

    # v = x1 mod n
    v = u1G_u2Q.x % (p)

    print(v, r)

    # verify signature
    if v == r:
        return True
    else:
        return False


# main program
if __name__ == '__main__':
    print("Curve E: y^2 = x^3 + ax + b (mod p)")

    # get the curve parameters
    p = 7559
    a = 0
    b = 7

    # get generator G
    G = Point(12, 217)

    # get public key Q
    Q = input("Enter public key Q: ").split()
    Q = Point(int(Q[0]), int(Q[1]))

    # verify public key
    if verify_public_key(Q, p, a, b):
        print("Public key is valid")
    else:
        print("Public key is invalid")
        exit()
    
    # get message M as input
    M = input("Enter message: ")

    # get signature (r, s)
    r = input("Enter r: ")
    s = input("Enter s: ")

    # verify signature
    if verify(G, Q, M, int(r), int(s), p, a, b):
        print("Signature is valid")
    else:
        print("Signature is invalid")
