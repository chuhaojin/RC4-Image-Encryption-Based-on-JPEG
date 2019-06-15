#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : rle.py
# @Time    : 2019/6/8 12:51
#@Software: PyCharm

import numpy as np


def rle_encode(order):
    rle_tuple, zero_num = [], 0
    for item in order:
        if item == 0 and zero_num <15:
            zero_num += 1
        else:
            rle_tuple.append((zero_num, item))
            zero_num = 0
    for i in range(len(rle_tuple) - 1, -1, -1):
        if rle_tuple[i][1] == 0:
            rle_tuple = rle_tuple[:i]
        else:
            break
    rle_tuple.append((0, 0))
    return rle_tuple

def rle_decode(tuple):
    order = []
    for item in tuple[:-1]:
        order = order + [0 for _ in range(item[0])] + [item[1]]
    order = order + [0 for _ in range(64 - len(order))]
    return order


if __name__ == "__main__":
    test = [35, 7, 0, 0, 0, -6, -2, 0, 0, -9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0,0,0,0,8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0,0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    rle_tuple = rle_encode(test)
    sequence = rle_decode(rle_tuple)
    print(rle_tuple)
    print(len(sequence))
    print(sequence)
    if test == sequence:
        print("equal")
