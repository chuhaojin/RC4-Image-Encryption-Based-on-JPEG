#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : zigzag.py
# @Time    : 2019/6/7 22:51
#@Software: PyCharm
import numpy as np

def zigzag_encode(array):
    height, width = len(array), len(array[0])
    flag, t = False, 0
    order = np.zeros(shape=[height * width], dtype=np.int)
    for i in range(height + width - 1):
        begin_y = min(i, height - 1)
        begin_x, flag = i - begin_y, ~flag
        while begin_y >= 0 and begin_x < width:
            order[t] = array[begin_y][begin_x] if flag else array[begin_x][begin_y]
            begin_y, begin_x, t = begin_y - 1, begin_x + 1, t + 1
    return order

def zigzag_decode(order):
    width = height = np.sqrt(len(order)).astype(int)
    flag, t = False, 0
    array = np.zeros(shape=[height, width], dtype=np.int)
    for i in range(height + width - 1):
        begin_y = min(i, height - 1)
        begin_x, flag = i - begin_y, ~flag
        while begin_y >= 0 and begin_x < width:
            if flag:
                array[begin_y][begin_x] = order[t]
            else:
                array[begin_x][begin_y] = order[t]
            begin_y, begin_x, t = begin_y - 1, begin_x + 1, t + 1
    return array

if __name__ == "__main__":
    test = np.array([[1, 2, 6, 7],
                     [3, 5, 8, 13],
                     [4, 9, 12, 14],
                     [10, 11, 15, 16]], dtype=np.int)
    sequence = zigzag_encode(test)
    array = zigzag_decode(sequence)
    if np.array_equal(array, test):
        print("equal")



