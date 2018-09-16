from functools import reduce


def gcd_list(num_list):
    return reduce(gcd, num_list)


def gcd(a, b):
    if b != 0:
        return gcd(b, a%b)
    else:
        return a


num_list = [14, 21, 77, 35]
print(gcd_list(num_list))
