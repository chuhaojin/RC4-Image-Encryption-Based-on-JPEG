#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : jpeg_decoder.py
# @Time    : 2019/6/10 11:07
#@Software: PyCharm

from models import loadimage, quantization, zigzag, rle, bit, sequence
from models.huffman import huffman_to_ldc, huffman_to_lac, huffman_to_cdc, huffman_to_cac
import cv2
from config import Qy, Qc, alpha
import numpy as np
from PIL import Image
from models import jpegFile

def layer_decode(byte_stream, Q=Qy, dc_func=huffman_to_ldc, ac_func=huffman_to_lac, alpha=1.0):
    # 解析比特流，获取bit编码
    bit_lists = sequence.sequence_decode(byte_stream, dc_func=dc_func, ac_func=ac_func)
    array_list = []
    # 计算量化系数
    Qa = np.maximum(Q * alpha, 1.0)
    for bit_list in bit_lists:
        # 对bit编码解码，获取rle编码
        rle_list = bit.bit_decode(bit_list)
        # 对rle编码进行解码，获取zigzag编码
        order = rle.rle_decode(rle_list)
        # 将zigzag型向量转为8*8矩阵
        array = zigzag.zigzag_decode(order)
        # 量化的逆操作
        inverse = quantization.inverse(array, Q=Qa)
        # 进行idct变换
        idct = cv2.idct(inverse)
        # 保存当前矩阵的计算结果
        array_list.append(idct)
    return array_list


def jpeg_decode(path, alpha=1.0):
    print("从文件中读取YCbCr数据流...")
    Y_byte_stream, Cb_byte_stream, Cr_byte_stream, shape = jpegFile.read_jpeg(read_path=path)
    print("读取YCbCr数据流成功！")
    print("解压YCbCr数据流...")
    y_list = layer_decode(Y_byte_stream, Q=Qy, dc_func=huffman_to_ldc, ac_func=huffman_to_lac, alpha=alpha)
    cb_list = layer_decode(Cb_byte_stream, Q=Qc, dc_func=huffman_to_cdc, ac_func=huffman_to_cac, alpha=alpha)
    cr_list = layer_decode(Cr_byte_stream, Q=Qc, dc_func=huffman_to_cdc, ac_func=huffman_to_cac, alpha=alpha)
    print("数据流解压成功！")
    print("合并8*8矩阵...")
    y = loadimage.img_merge(y_list, shape=shape[:2])
    cb = loadimage.img_merge(cb_list, shape=shape[:2])
    cr = loadimage.img_merge(cr_list, shape=shape[:2])
    print("8*8矩阵合并成功！")
    print("将YCbCr图像转成gbr..")
    img = loadimage.get_bgr(y, cb, cr)
    print("图像解压成功！大小为：", img.shape)
    image = Image.fromarray(img)
    image.show()
    return img[:shape[0], :shape[1]]


if __name__ == "__main__":
    path = "data/jch.jpg"
    img = jpeg_decode(path, alpha=alpha)


