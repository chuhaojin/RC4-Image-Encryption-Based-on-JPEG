#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : decryption.py
# @Time    : 2019/6/12 19:23
#@Software: PyCharm

from models import loadimage, quantization, zigzag, rle, bit, sequence
from models.huffman import huffman_to_ldc, huffman_to_lac, huffman_to_cdc, huffman_to_cac
import cv2
from config import Qy, Qc, alpha
import numpy as np
from PIL import Image
from encryption import get_key
from models import rc4
from models import jpegFile


def decryption_q(q_list, key, en_rank):
    length = len(q_list[0])
    x = [t % length for t in range(en_rank) for _ in range(en_rank - t)]
    y = [(en_rank - i - 1) % length for t in range(en_rank) for i in range(en_rank - t)]
    for i in range(len(x)):
        try:
            q_string = "".join([chr(q[x[i], y[i]]) for q in q_list])
            encry_q = rc4.rc4(q_string, key)
            for t in range(len(q_list)):
                q_list[t][x[i], y[i]] = ord(encry_q[t]) - 500
        except:
            pass
    return q_list

def layer_decryption(byte_stream, key, en_rank, Q=Qy, dc_func=huffman_to_ldc, ac_func=huffman_to_lac, alpha=1.0):
    bit_lists = sequence.sequence_decode(byte_stream, dc_func=dc_func, ac_func=ac_func)
    array_list, q_list  = [], []
    Qa = np.maximum(Q * alpha, 1.0)
    for bit_list in bit_lists:
        rle_list = bit.bit_decode(bit_list)
        order = rle.rle_decode(rle_list)
        q = zigzag.zigzag_decode(order)
        q_list.append(q)
    q_list = decryption_q(q_list, key, en_rank)
    for q in q_list:
        inverse = quantization.inverse(q, Q=Qa)
        idct = cv2.idct(inverse)
        array_list.append(idct)
    return array_list


def jpeg_decryption(read_path, key, en_rank, alpha=1.0):
    print("从文件中读取YCbCr数据流...")
    Y_byte_stream, Cb_byte_stream,Cr_byte_stream, shape = jpegFile.read_jpeg(read_path)
    print("读取YCbCr数据流成功！")
    print("解压YCbCr数据流并解密量化矩阵...")
    y_list = layer_decryption(Y_byte_stream, key, en_rank, Q=Qy,
                              dc_func=huffman_to_ldc, ac_func=huffman_to_lac, alpha=alpha)
    cb_list = layer_decryption(Cb_byte_stream, key, en_rank, Q=Qc,
                               dc_func=huffman_to_cdc, ac_func=huffman_to_cac, alpha=alpha)
    cr_list = layer_decryption(Cr_byte_stream, key, en_rank, Q=Qc,
                               dc_func=huffman_to_cdc, ac_func=huffman_to_cac, alpha=alpha)
    print("解密完成！合并8*8矩阵...")
    y = loadimage.img_merge(y_list, shape=shape[:2])
    cb = loadimage.img_merge(cb_list, shape=shape[:2])
    cr = loadimage.img_merge(cr_list, shape=shape[:2])
    print("合并8*8矩阵成功！")
    print("YCbCr图像转bgr图像...")
    img = loadimage.get_bgr(y, cb, cr)
    print("图像解密完成！大小为：", img.shape)
    image = Image.fromarray(img)
    image.show()
    return img[:shape[0], :shape[1]]


if __name__ == "__main__":
    read_path = "data/encryption.jpg"
    key_len = 64
    en_rank = 2
    key = get_key(key_len)
    wrong_key = get_key(key_len)
    print("key:", key)
    print("wrong key:", wrong_key)
    img = jpeg_decryption(read_path, key, en_rank, alpha=alpha)
    img2 = jpeg_decryption(read_path, wrong_key, en_rank, alpha=alpha)

