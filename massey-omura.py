# import all functions from ecc_func.py
from ecc_func import * 


# Massey-Omura encryption
def algorithm(M, p, a, b):
    
    m_A = secrets.randbelow(exclusive_upper_bound=p) + 1
    while gcd(m_A, p) != 1:
        m_A = secrets.randbelow(exclusive_upper_bound=p) + 1

    m_B = secrets.randbelow(exclusive_upper_bound=p) + 1
    while gcd(m_B, p) != 1:
        m_B = secrets.randbelow(exclusive_upper_bound=p) + 1
    
    # Compute m_A * M
    m_A_M = ec_mult(m_A, M, p, a, b)
    print(f'm_A.M = ({m_A_M.x}, {m_A_M.y})')

    # Compute m_B * m_A_M
    m_B_m_A_M = ec_mult(m_B, m_A_M, p, a, b)
    print(f'm_B.m_A.M = ({m_B_m_A_M.x}, {m_B_m_A_M.y})')

    # Compute m_A^(-1) * m_B * m_A_M
    m_A_inv = pow(m_A, -1, p)
    m_A_inv_m_B_m_A_M = ec_mult(m_A_inv, m_B_m_A_M, p, a, b)
    print(f'm_A^(-1).m_B.m_A.M = ({m_A_inv_m_B_m_A_M.x}, {m_A_inv_m_B_m_A_M.y})')

    # Compute m_B^(-1) * m_A^(-1) * m_B * m_A_M
    m_B_inv = pow(m_B, -1, p)
    m_B_inv_m_A_inv_m_B_m_A_M = ec_mult(m_B_inv, m_A_inv_m_B_m_A_M, p, a, b)
    print(f'm_B^(-1).m_A^(-1).m_B.m_A.M = ({m_B_inv_m_A_inv_m_B_m_A_M.x}, {m_B_inv_m_A_inv_m_B_m_A_M.y})')


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

    # perform encryption-decryption
    algorithm(M, p, a, b)
