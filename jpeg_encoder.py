#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : jpeg_encoder.py
# @Time    : 2019/6/10 9:05
#@Software: PyCharm

from models import loadimage, quantization, zigzag, rle, bit, sequence
from models.huffman import ldc_to_huffman, lac_to_huffman, cdc_to_huffman, cac_to_huffman
import cv2
from config import Qy, Qc, alpha
import numpy as np
from models.jpegFile import write_jpeg

def layer_encode(layer, dc_func, ac_func, Q, alpha=1.0):
    # 图像分割为8*8矩阵
    array_list = loadimage.img_split(img=layer)
    byte_stream = ''
    Qa = np.maximum(Q * alpha, 1.0)
    for array in array_list:
        # 矩阵进行dct变换
        dct = cv2.dct(array)
        # 量化
        q = quantization.quantization(dct, Q=Qa)
        # zigzag型变换
        order = zigzag.zigzag_encode(q)
        # rle编码
        rle_list = rle.rle_encode(order)
        # bit编码
        bit_list = bit.bit_encode(rle_list)
        # 将bit编码转化为哈夫曼序列，并转化为比特流
        seq = sequence.sequence_encode(bit_list, dc_func=dc_func, ac_func=ac_func)
        # 该矩阵的比特流与前面的矩阵比特流拼接
        byte_stream = byte_stream + seq
    return byte_stream


def jpeg_encode(img_path, write_path, alpha=1.0):
    print("加载图片...")
    img = loadimage.get_image(img_path)
    print("图像加载成功！形状为：", img.shape)
    # Y, Cb, Cr = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    print("图像转YCbCr格式...")
    Y, Cb, Cr = loadimage.get_YCbCr(img)
    print("图像转YCbCr格式成功！")
    # img2 = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    # Y, Cr, Cb = img2[:, :, 0], img2[:, :, 1], img2[:, :, 2]
    print("对YCbCr图像压缩...")
    # 压缩Y层，返回结果为比特流
    Y_byte_stream = layer_encode(Y, Q=Qy, dc_func=ldc_to_huffman, ac_func=lac_to_huffman, alpha=alpha)
    # 压缩Cb层，返回结果为比特流
    Cb_byte_stream = layer_encode(Cb, Q=Qc, dc_func=cdc_to_huffman, ac_func=cac_to_huffman, alpha=alpha)
    # 压缩Cr层，返回结果为比特流
    Cr_byte_stream = layer_encode(Cr, Q=Qc, dc_func=cdc_to_huffman, ac_func=cac_to_huffman, alpha=alpha)
    print("YCbCr图像压缩完成！")
    print("写文件...")
    write_jpeg(write_path=write_path, y=Y_byte_stream, cb=Cb_byte_stream, cr=Cr_byte_stream, shape=img.shape)
    print("写文件成功！")
    # 将三个比特流直接返回，可用与扩展操作
    return Y_byte_stream, Cb_byte_stream, Cr_byte_stream


if __name__ == "__main__":
    img_path = "data/test.jpg"
    write_path = "data/jch.jpg"
    Y_byte_stream, Cb_byte_stream, Cr_byte_stream = jpeg_encode(img_path=img_path, write_path=write_path, alpha=alpha)
    # print((len(Y_byte_stream) + len(Cb_byte_stream) + len(Cr_byte_stream)) // 8 // 1024)
    # print(time.time() - time_0)
    # img = loadimage.get_image(path=path)
    # Y, Cb, Cr = loadimage.get_YCbCr(image=img)
    # Y_byte_stream = layer_encode(Y, Q=Qy, dc_func=ldc_to_huffman, ac_func=lac_to_huffman, alpha=alpha)
    # Cb_byte_stream = layer_encode(Cb, Q=Qc, dc_func=cdc_to_huffman, ac_func=cac_to_huffman, alpha=alpha)
    # Cr_byte_stream = layer_encode(Cr, Q=Qc, dc_func=cdc_to_huffman, ac_func=cac_to_huffman, alpha=alpha)
