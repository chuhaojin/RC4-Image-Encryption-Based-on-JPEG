#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : dct.py
# @Time    : 2019/6/7 15:56
#@Software: PyCharm

import numpy as np


def dct(array, m):
    length = len(array)
    Fm = np.sum(array * [np.cos(np.pi / length * m * (i + 1/2)) for i in range(length)])
    return Fm


def idct(array, m):
    length = len(array)
    cosine = [np.cos(np.pi / length * (m + 1/2)*k) for k in range(1, length)]
    Xm = array[0]/length + np.sum((2 * array[1:] / length) * cosine)
    return Xm


def dct_array(array):
    result = []
    for i in range(len(array)):
        result.append(dct(array, i))
    return np.array(result)


def idct_array(array):
    result = []
    for i in range(len(array)):
        result.append(idct(array, i))
    return np.array(result)


def alpha(x, X):
    return 1/np.sqrt(X) if x==0 else np.sqrt(2/X)


def cosine(x, u, M):
    return np.cos((2 * x + 1) * u * np.pi / (2 * M))


def dct2d_kernel(value, x, y, u, v, M, N):
    return value * cosine(x, u, M) * cosine(y, v, N)


def idct2d_kernel(value, x, y, u, v, M, N):
    return alpha(u, M) * alpha(v, N) * dct2d_kernel(value, x, y, u, v, M, N)


def dct2d(array, u, v):
    M, N = len(array), len(array[0])
    alpha_u, alpha_v = alpha(u, M), alpha(v, N)
    temp = np.sum([np.sum([dct2d_kernel(array[x, y], x, y, u, v, M, N) for y in range(N)]) for x in range(M)])
    return alpha_u * alpha_v * temp


def idct2d(array, x, y):
    M, N = len(array), len(array[0])
    temp = np.sum([np.sum([idct2d_kernel(array[u, v], x, y, u, v, M, N) for v in range(N)]) for u in range(M)])
    return np.rint(temp).astype(int)


def dct2d_array(array):
    return np.array([[dct2d(array, x, y) for y in range(len(array[0]))] for x in range(len(array))])


def idct2d_array(array):
    return np.array([[idct2d(array, x, y) for y in range(len(array[0]))] for x in range(len(array))])


if __name__ == "__main__":
    array = np.array([50,55,67,80,-10,-5,20,30])
    array_2d = np.array([[34, 34, 34, 33, 34, 28, 35, 32],
                         [34, 34, 34, 33, 34, 28, 35, 32],
                         [34, 34, 34, 33, 34, 28, 35, 32],
                         [34, 34, 34, 33, 34, 28, 35, 32],
                         [34, 34, 34, 33, 34, 28, 35, 32],
                         [36, 36, 29, 27, 33, 31, 30, 31],
                         [32, 32, 35, 30, 32, 33, 31, 27],
                         [30, 30, 27, 28, 30, 30, 28, 29]])
    result = dct2d_array(array_2d)
    print(result)
    print(idct2d_array(result))
    # i_array = dct_array(array)
    # print("dct 0:", dct(array, 0))
    # print("dct array:", i_array)
    # print("idct array:", idct_array(i_array))
