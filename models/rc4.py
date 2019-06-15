#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : rc4.py
# @Time    : 2019/6/15 16:29
#@Software: PyCharm

def rc4(data, key):
    bit_length = 512
    """RC4 encryption and decryption method."""
    S, j, out = list(range(bit_length)), 0, []

    for i in range(bit_length):
        j = (j + S[i] + ord(key[i % len(key)])) % bit_length
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for ch in data:
        i = (i + 1) % bit_length
        j = (j + S[i]) % bit_length
        S[i], S[j] = S[j], S[i]
        out.append(chr(ord(ch) ^ S[(S[i] + S[j]) % bit_length]))

    return "".join(out)

if __name__ == "__main__":
    buf = rc4("Hello World", "rc4")
    assert rc4(buf, "rc4") == "Hello World"
    print("Ran 1 test..")
