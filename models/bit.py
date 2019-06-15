#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : bit.py
# @Time    : 2019/6/9 16:06
#@Software: PyCharm

from models.huffman import huffman_to_num, num_to_huffman

def dc_bit_encode(rle_tuple):
    huffman_code = num_to_huffman(rle_tuple[1])
    return (len(huffman_code), huffman_code)


def dc_bit_decode(bit_tuple):
    num = huffman_to_num(bit_tuple[1])
    return (0, num)


def ac_bit_encode(rle_tuple):
    huffman_code = num_to_huffman(rle_tuple[1])
    return (hex(rle_tuple[0])[2:] + hex(len(huffman_code))[2:], huffman_code)


def ac_bit_decode(bit_tuple):
    num = huffman_to_num(bit_tuple[1])
    return (int(bit_tuple[0][0], base=16), num)


def bit_encode(rle_list):
    bit_list = []
    bit_list.append(dc_bit_encode(rle_list[0]))
    for item in rle_list[1:]:
        bit_list.append(ac_bit_encode(item))
    return bit_list

def bit_decode(bit_list):
    rle_list = []
    rle_list.append(dc_bit_decode(bit_list[0]))
    for item in bit_list[1:]:
        rle_list.append(ac_bit_decode(item))
    return rle_list


if __name__ == "__main__":
    test = [(0, 35), (0, 7), (3, -6), (0, -2), (2, -9), (15, 0), (2, 8), (0, 0)]
    bit = bit_encode(test)
    print(bit)
    rle = bit_decode(bit)
    print(rle)