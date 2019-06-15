#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : quantization.py
# @Time    : 2019/6/7 21:36
#@Software: PyCharm

import numpy as np
from config import Qc, Qy


def quantization(array, Q, alpha=1.0):
    if alpha==1.0:
        return np.rint(array / Q).astype(int)
    else:
        return np.rint(array / (Q * alpha)).astype(int)


def inverse(array, Q, alpha=1.0):
    if alpha == 1.0:
        return array * Q
    else:
        return array * (alpha * Q)


if __name__ == "__main__":
    import cv2
    from models.zigzag import array_to_order, order_to_array
    alpha = 0.005
    array_2d = np.array([[-415.38, -30.19, -61.20, 27.24, 56.12, -20.10, -2.39, 0.46],
                         [4.47, -21.86, -60.76, 10.25, 13.15, -7.09, -8.54, 4.88],
                         [-46.83, 7.37, 77.13, -24.56, -28.91, 9.93, 5.42, -5.65],
                         [-48.53, 12.07, 34.10, -14.76, -10.24, 6.30, 1.83, 1.95],
                         [12.12, -6.55, -13.20, -3.95, -1.87, 1.75, -2.79, 3.14],
                         [-7.73, 2.91, 2.38, -5.94, -2.38, 0.94, 4.30, 1.85],
                         [-1.03, 0.18, 0.42, -2.42, -0.88, -3.02, 4.12, -0.66],
                         [-0.17, 0.14, -1.07, -4.19, -1.17, -0.1, 0.5, 1.68]])
    # array_2d = np.array([[34, 34, 34, 33, 34, 28, 35, 32],
    #                      [34, 34, 34, 33, 34, 28, 35, 32],
    #                      [34, 34, 34, 33, 34, 28, 35, 32],
    #                      [34, 34, 34, 33, 34, 28, 35, 32],
    #                      [34, 34, 34, 33, 34, 28, 35, 32],
    #                      [36, 36, 29, 27, 33, 31, 30, 31],
    #                      [32, 32, 35, 30, 32, 33, 31, 27],
    #                      [30, 30, 27, 28, 30, 30, 28, 29]])
    # array_2d = dct2d_array(array_2d)
    result = quantization(array_2d, Q=Qy, alpha=alpha)
    order = array_to_order(result)
    result = order_to_array(order)
    inverse_array = inverse(result, Q=Qy, alpha=alpha)
    print(array_2d - inverse_array)

