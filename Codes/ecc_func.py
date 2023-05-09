from collections import namedtuple
from math import ceil, sqrt
import random
import secrets
import time


Point = namedtuple("Point", "x y")

# The point at infinity (origin for the group law).
O = 'Origin'

# Choose a particular curve and prime.  We assume that p > 3.
# Chosen curve -> y^2 = x^3 + ax + b (mod p)


def isprime(p):
    """
    Primality testing using AKS algorithm.
    """
    if p == 2:
        return True
    if p == 3:
        return True
    if p % 2 == 0:
        return False
    if p % 3 == 0:
        return False

    r = 5
    while r*r <= p:
        if p % r == 0:
            return False
        if p % (r+2) == 0:
            return False
        r += 6
    return True


def gcd(a, b):
    """
    Euclid's algorithm for determining the greatest common divisor.
    """
    while b != 0:
        a, b = b, a % b
    return a


def get_curve():
    """
    Returns the curve parameters a, b and the prime p
    E: y^2 = x^3 + ax + b (mod p)
    """
    p = int(input("Enter the prime p: "))
    while not isprime(p):
        p = int(input("Enter the prime p: "))
    a = int(input("Enter the coefficient a: "))
    b = int(input("Enter the coefficient b: "))

    return p, a, b


def valid(P, p, a, b):
    """
    Determine whether we have a valid representation of a point
    on our curve.  We assume that the x and y coordinates
    are always reduced modulo p, so that we can compare
    two points for equality with a simple ==.
    """
    if P == O:
        return True
    else:
        return (
            (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and
            0 <= P.x < p and 0 <= P.y < p)


def inv_mod_p(x, p):
    """
    Compute an inverse for x modulo p, assuming that x
    is not divisible by p.
    """
    if x % p == 0:
        raise ZeroDivisionError("Impossible inverse")
    return pow(x, p-2, p)


def ec_inv(P, p, a, b):
    """
    Inverse of the point P on the elliptic curve y^2 = x^3 + ax + b.
    """
    if P == O:
        return P
    return Point(P.x, (-P.y)%p)


def ec_add(P, Q, p, a, b):
    """
    Sum of the points P and Q on the elliptic curve y^2 = x^3 + ax + b.
    """
    if not (valid(P, p, a, b) and valid(Q, p, a, b)):
        raise ValueError("Invalid inputs")

    # Deal with the special cases where either P, Q, or P + Q is
    # the origin.
    if P == O:
        result = Q
    elif Q == O:
        result = P
    elif Q == ec_inv(P, p, a, b):
        result = O
    else:
        # Cases not involving the origin.
        if P == Q:
            dydx = (3 * P.x**2 + a) * inv_mod_p(2 * P.y, p)
        else:
            dydx = (Q.y - P.y) * inv_mod_p(Q.x - P.x, p)
        x = (dydx**2 - P.x - Q.x) % p
        y = (dydx * (P.x - x) - P.y) % p
        result = Point(x, y)

    # The above computations *should* have given us another point
    # on the curve.
    assert valid(result, p, a, b)
    return result


def ec_mult(n, P, p, a, b):
    """
    Multiply the point P by the integer n using
    the successive doubling algorithm.
    """
    Q = O
    while n > 0:
        if n % 2 == 1:
            Q = ec_add(Q, P, p, a, b)
        P = ec_add(P, P, p, a, b)
        n //= 2
    return Q


def generator_point(p, a, b):
    """
    Returns a generator point on the elliptic curve y^2 = x^3 + ax + b.
    """
    # The curve should have at least one point on it.
    while True:
        x = secrets.randbelow(p)
        y2 = (x**3 + a*x + b) % p
        y = sqrt(y2)
        if int(y) == y:
            return Point(x, int(y))


def get_ciphertext():
    """
    Returns the ciphertext (C1, C2) from the recipient
    """
    C1_x, C1_y = input("Enter coordinates of Cipher C1: ").split()
    C2_x, C2_y = input("Enter coordinates of Cipher C2: ").split()

    C1 = Point(int(C1_x), int(C1_y))
    C2 = Point(int(C2_x), int(C2_y))

    return C1, C2


def get_private_key():
    """
    Returns the private key k
    """
    k = int(input("Enter the private key k: "))

    return k
