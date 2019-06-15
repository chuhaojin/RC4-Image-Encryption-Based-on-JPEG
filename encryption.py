#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : encryption.py
# @Time    : 2019/6/12 9:09
#@Software: PyCharm

import numpy as np
from models import rc4
import random
import string
from models import loadimage, quantization, zigzag, rle, bit, sequence
from models.huffman import ldc_to_huffman, lac_to_huffman, cdc_to_huffman, cac_to_huffman
import cv2
from config import Qy, Qc, alpha
from jpeg_decoder import jpeg_decode
from models import jpegFile

random.seed(1024)

def get_key(key_len):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(key_len))


def encryption_q(q_list, key, en_rank):
    length = len(q_list[0])
    x = [t % length for t in range(en_rank) for _ in range(en_rank - t)]
    y = [(en_rank - i - 1) % length for t in range(en_rank) for i in range(en_rank - t)]
    for i in range(len(x)):
        q_string = "".join([chr(q[x[i], y[i]] + 500) for q in q_list])
        encry_q = rc4.rc4(q_string, key)
        for t in range(len(q_list)):
            q_list[t][x[i], y[i]] = ord(encry_q[t])
    return q_list

def layer_encryption(layer, key, en_rank, dc_func, ac_func, Q, alpha=1.0):
    array_list = loadimage.img_split(img=layer)
    byte_stream = ''
    Qa = np.maximum(Q * alpha, 1.0)
    q_list = []
    '''获得每个8*8矩阵的量化矩阵'''
    for array in array_list:
        dct = cv2.dct(array)
        q = quantization.quantization(dct, Q=Qa)
        q_list.append(q)
    q_list = encryption_q(q_list, key, en_rank)
    for q in q_list:
        order = zigzag.zigzag_encode(q)
        rle_list = rle.rle_encode(order)
        bit_list = bit.bit_encode(rle_list)
        seq = sequence.sequence_encode(bit_list, dc_func=dc_func, ac_func=ac_func)
        byte_stream = byte_stream + seq
    return byte_stream


def jpeg_encryption(img_path, write_path, key, en_rank, alpha=1.0):
    print("加载图片...")
    img = loadimage.get_image(img_path)
    print("图像加载成功！形状为：", img.shape)
    # Y, Cb, Cr = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    print("图像转YCbCr格式...")
    Y, Cb, Cr = loadimage.get_YCbCr(img)
    print("图像转YCbCr格式成功！")
    print("对YCbCr图像压缩并加密...")
    Y_byte_stream = layer_encryption(Y, key, en_rank, Q=Qy,
                                     dc_func=ldc_to_huffman, ac_func=lac_to_huffman, alpha=alpha)
    Cb_byte_stream = layer_encryption(Cb, key, en_rank, Q=Qc,
                                      dc_func=cdc_to_huffman, ac_func=cac_to_huffman, alpha=alpha)
    Cr_byte_stream = layer_encryption(Cr, key, en_rank, Q=Qc,
                                      dc_func=cdc_to_huffman, ac_func=cac_to_huffman, alpha=alpha)
    print("YCbCr图像加密完成！")
    print("写文件...")
    jpegFile.write_jpeg(write_path=write_path, y=Y_byte_stream,
                        cb=Cb_byte_stream, cr=Cr_byte_stream, shape=img.shape)
    print("写文件成功！")
    return Y_byte_stream, Cb_byte_stream, Cr_byte_stream


if __name__ == "__main__":
    img_path = "data/lenna.jpg"
    write_path = "data/encryption.jpg"
    key_len = 64
    en_rank = 2
    key = get_key(key_len)
    print("key:", key)
    Y_byte_stream, Cb_byte_stream, Cr_byte_stream = jpeg_encryption(img_path, write_path, key, en_rank, alpha)
    img = jpeg_decode(write_path, alpha=alpha)
