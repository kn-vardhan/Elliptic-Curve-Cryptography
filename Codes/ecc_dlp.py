"""
This file contains functions to solve discrete logs on elliptic curves.
It consists of the following algorithms:
1. Baby step, Giant step method
2. Pollard's rho method
3. Pohlig-Hellman method

"""

import sys

sys.path.append("C:/Users/Anita Dash/Downloads")

import ecc_func as ecc
import math
import random

inf = ecc.Point(0, 0)


# Baby step, Giant step method to find order of point P
# Function that returns list of prime factors of M
def prime_factors(n):
    factors = []
    divisor = 2
    while divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        else:
            divisor += 1
    return list(set(factors))


def order_point(P, p, a, b):
    Q = ecc.ec_mult(p + 1, P, p, a, b)
    m = math.ceil(p ** (1 / 4))
    jp = []
    negjp = []
    M = 0
    for j in range(0, m + 1):
        jp.append(ecc.ec_mult(j, P, p, a, b))
        negjp.append(ecc.ec_inv(jp[j], p, a, b))
    m2P = ecc.ec_mult(2 * m, P, p, a, b)
    for k in range(-m, m + 1):
        k2mP = ecc.ec_mult(k, m2P, p, a, b)
        Qsum = ecc.ec_add(Q, k2mP, p, a, b)
        if Qsum in jp:
            ind = jp.index(Qsum)
            M = p + 1 + 2 * m * k - ind
            break
        elif Qsum in negjp:
            ind = negjp.index(Qsum)
            M = p + 1 + 2 * m * k + ind
            break
    flag = 0
    while flag == 0:
        pf = prime_factors(M)
        for i in range(len(pf)):
            if ecc.ec_mult(M // pf[i], P, p, a, b) == inf:
                M = M // pf[i]
                break
            if i == len(pf) - 1:
                flag = 1
    return M


# Baby Step, Giant step method to solve discrete logs
def BG(P, Q, p, a, b):
    k = -1
    m = math.ceil(math.sqrt(p + 1 + 2 * math.sqrt(p)))
    mP = ecc.ec_mult(m, P, p, a, b)
    ip = []
    for i in range(1, m):
        ip.append(ecc.ec_mult(i, P, p, a, b))
    for j in range(0, m):
        jmP = ecc.ec_mult(j, mP, p, a, b)
        negjmP = ecc.ec_inv(jmP, p, a, b)
        diff = ecc.ec_add(Q, negjmP, p, a, b)
        if diff in ip:
            ind = ip.index(diff) + 1
            k = ind + j * m
            break
    return k


# Pollard's Rho method to solve discrete logs
def calc_val(P, Q, coeff, p, a, b):
    U = coeff[0]
    V = coeff[1]
    Val = ecc.ec_add(ecc.ec_mult(U, P, p, a, b), ecc.ec_mult(V, Q, p, a, b), p, a, b)
    return Val


def pollard(P, Q, p, a, b):
    order = order_point(P, p, a, b)
    points = []
    val = []
    points.append([random.randint(0, order - 1), random.randint(0, order - 1)])
    val.append(calc_val(P, Q, points[0], p, a, b))
    M0 = [random.randint(0, order - 1), random.randint(0, order - 1)]
    M1 = [random.randint(0, order - 1), random.randint(0, order - 1)]
    M2 = [random.randint(0, order - 1), random.randint(0, order - 1)]
    i = 0
    cnt = 0
    k = 0
    while a <= order:
        if val[i].x % 3 == 0:
            points.append([(points[i][0] + M0[0]) % order, (points[i][1] + M0[1]) % order])
        elif val[i].x % 3 == 1:
            points.append([(points[i][0] + M1[0]) % order, (points[i][1] + M1[1]) % order])
        elif val[i].x % 3 == 2:
            points.append([(points[i][0] + M2[0]) % order, (points[i][1] + M2[1]) % order])
        value = calc_val(P, Q, points[i + 1], p, a, b)
        if value in val:
            cnt += 1
            ind = val.index(value)
            diff = [(points[i + 1][0] - points[ind][0]) % order, (points[i + 1][1] - points[ind][1]) % order]
            d = math.gcd(diff[1], order)
            mod = order // d
            if math.gcd(diff[1], mod) != 1:
                k = -1
                break
            k = (pow(diff[1], -1, mod) * (-diff[0])) % mod
            mult = ecc.ec_mult(k, P, p, a, b)
            if mult == Q:
                break
        val.append(value)
        i += 1

    return k


# Pohlig-Hellman Method to solve discrete logs

# function for finding prime factors of a number and their highest power that divides the number
def prime_factor_power(n):
    prime = []
    power = []
    i = 2
    while i * i <= n:
        if n % i == 0:
            prime.append(i)
            cnt = 0
            while n % i == 0:
                n = n // i
                cnt += 1
            power.append(cnt)
        i += 1
    if n > 1:
        prime.append(n)
        power.append(1)
    return prime, power


def crt(k_list, prime_list):
    N = 1
    for prime in prime_list:
        N *= prime

    x = 0
    for i in range(len(k_list)):
        Ni = N // prime_list[i]
        xi = pow(Ni, -1, prime_list[i])
        x += k_list[i] * xi * Ni

    return x % N


def Pohlig(P, Q, N, p, a, b):
    prime_list, power_val = prime_factor_power(N)
    count = 0
    k = []
    for q in prime_list:
        T = []
        for j in range(0, q):
            val = ecc.ec_mult((N // q), P, p, a, b)
            T.append(ecc.ec_mult(j, val, p, a, b))
        Q_list = [Q]
        k_list = []
        q_val = ecc.ec_mult((N // q), Q, p, a, b)
        if q_val in T:
            ind = T.index(q_val)
            k_list.append(ind)
        e = power_val[count]
        for r in range(1, e):
            Q_r_minus = Q_list[r - 1]
            k_r_minus = ecc.ec_mult(k_list[r - 1] * pow(q, r - 1), P, p, a, b)
            neg_k_r_minus = ecc.ec_inv(k_r_minus, p, a, b)
            Q_r = ecc.ec_add(Q_r_minus, neg_k_r_minus, p, a, b)
            Q_list.append(Q_r)
            q_val = ecc.ec_mult((N // pow(q, r + 1)), Q_r, p, a, b)
            if q_val in T:
                ind = T.index(q_val)
                k_list.append(ind)
        k_sum = 0
        for i in range(0, e):
            k_sum = k_sum + k_list[i] * pow(q, i) % pow(q, e)
        k.append(k_sum)
        count += 1
    for i in range(len(prime_list)):
        prime_list[i] = prime_list[i] ** power_val[i]

    # chinese remainder theorem for finding k
    k = crt(k, prime_list)
    return k
