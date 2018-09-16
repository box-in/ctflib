from functools import reduce
import binascii
import numpy as np
import math
import time


def ext_gcd(a, b):
    if b > 0:
        y, x, d = ext_gcd(b, a % b)
        return x, y - a // b * x, d
    else:
        return 1, 0, a


def gcd_list(num_list):
    return reduce(gcd, num_list)


def gcd(a, b):
    if b != 0:
        return gcd(b, a%b)
    else:
        return a


def lcm(a, b):
    return a // gcd(a, b) * b


def lcm_list(num_list):
    return reduce(lcm, num_list)


def is_prime(n):
    i = 2
    while i * i < n:
        if n % i == 0:
            return False
        i += 1
    return True


def pf_decomposition(n):
    """
    10**12 : 0.7sec
    10**13 : 1.3sec
    10**14 : 6.4sec
    practicality factor is 14 digit or less
    sqrt(n)
    """
    i = 2
    factor = []
    while i ** 2 < n:
        e = 0
        while n % i == 0:
            n //= i
            e += 1
        if e > 0:
            factor.append([i, e])
        i += 1
    if n > 0:
        factor.append([n, 1])
    return factor


def generate_rsa_key(e=65537, p=299681192390656691733849646142066664329, q=324144336644773773047359441106332937713):
    key, _, _ = ext_gcd(e, (p-1)*(q-1))
    return int(key % ((p-1)*(q-1)))


def encrypt_rsa(plain, e=65537, n=97139961312384239075080721131188244842051515305572003521287545456189235939577):
    """
    :param plain:
    :param n: public key1
    :param e: public key2
    :return:
    """
    crypto = pow(plain, e, n)
    return crypto


def decrypt_rsa(crypto, d, n=97139961312384239075080721131188244842051515305572003521287545456189235939577):
    """
    :param crypto:
    :param d: secret key
    :param n: public key
    :return:
    """
    dec = pow(crypto, d, n)
    return dec


def main():
    pass

if __name__  == "__main__":
    main()
