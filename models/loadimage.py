#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : loadimage.py
# @Time    : 2019/6/8 19:58
#@Software: PyCharm
from PIL import Image
import numpy as np
from models.quantization import quantization, inverse
from config import Qc, Qy
import cv2

def get_image(path):
    return cv2.imread(path)


def get_YCbCr(image):
    Y = 0.257 * image[:, :, 0] + 0.504 * image[:, :, 1] + 0.098 *image[:, :, 2] + 16
    Cb = -0.148 * image[:, :, 0] - 0.291 * image[:, :, 1] + 0.439 * image[:, :, 2] + 128
    Cr = 0.439 * image[:, :, 0] - 0.368 * image[:, :, 1] - 0.071 * image[:, :, 2] + 128
    return Y.astype(np.uint8), Cb.astype(np.uint8), Cr.astype(np.uint8)


def get_rgb(Y, Cb, Cr):
    R = 1.164 * (Y - 16) + 1.596 * (Cr - 128)
    G = 1.164 * (Y - 16) - 0.392 * (Cb - 128) - 0.813 * (Cr - 128)
    B = 1.164 * (Y - 16) + 2.017 * (Cb - 128)
    img = np.zeros(shape=(R.shape[0], R.shape[1], 3)).astype(np.uint8)
    img[:, :, 0], img[:, :, 1], img[:, :, 2] = G, B, R
    return img


def get_bgr(y, cb, cr):
    img = np.zeros(shape=(y.shape[0], y.shape[1], 3), dtype=np.uint8)
    img[:, :, 0], img[:, :, 1], img[:, :, 2] = y, cr, cb
    img = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)
    return img


def padding(img):
    shape = img.shape
    height = shape[0] + (8 - shape[0])% 8
    width = shape[1] + (8 - shape[1]) % 8
    pad = np.zeros(shape=[height, width])
    pad[:shape[0], :shape[1]] = img
    pad[shape[0]:, :shape[1]] = img[shape[0] - 1:, :]
    pad[:shape[0], shape[1]:] = img[:, shape[1] - 1:]
    pad[shape[0]:, shape[1]:] = img[shape[0] - 1, shape[1] - 1]
    return pad


def img_split(img):
    pad = padding(img)
    height, width = pad.shape
    result = [pad[i: i + 8, j: j + 8] for i in range(0, height, 8) for j in range(0, width, 8)]
    return np.array(result)


def img_merge(array_list, shape):
    height = shape[0] + (8 - shape[0]) % 8
    width = shape[1] + (8 - shape[1]) % 8
    pad = np.zeros(shape=(height, width))
    t = 0
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            pad[i : i + 8, j : j+8] = array_list[t]
            t += 1
    return pad[:shape[0], :shape[1]]


def layer_test(layer, Q, alpha, shape):
    Qa = np.maximum(Q * alpha, 1.0)
    array_list = img_split(img=layer)
    v_array = []
    for array in array_list:
        dct = cv2.dct(array)
        q = quantization(dct, Q=Qa)
        inv = inverse(q, Q=Qa)
        v_array.append(cv2.idct(inv))
    v_layer = img_merge(v_array, shape=shape[:2])
    return v_layer


def test(path, times, alpha=1.0):
    img = get_image(path)
    shape = img.shape
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    for _ in range(times):
        B = layer_test(B, Qy, alpha=alpha, shape=shape)
        G = layer_test(G, Qc, alpha, shape)
        R = layer_test(R, Qc, alpha, shape)
    img[:, :, 0], img[:, :, 1], img[:, :, 2] = R, G, B
    cv2.imshow("v_img", img)
    cv2.waitKey(0)
    return


if __name__ == "__main__":
    path = "../data/test.jpg"
    test(path, times=10, alpha=0.1)
    # import cv2
    # cv2.imshow("y", Y.astype(np.uint8))
    # cv2.imshow("cb", Cb.astype(np.uint8))
    # cv2.imshow("cr", Cr.astype(np.uint8))
    # img2 = get_rgb(Y, Cb, Cr)
    # cv2.imshow("img2", img2)
    # cv2.waitKey(0)
    # dct = cv2.dct(result[0])
    # idct = cv2.idct(dct)
    # print(result[0])
    # print(idct)
    # if np.array_equal(result[0], idct):
    #     print("dct idct equal.")
    # print(result[0] - idct)


    # print(result)


