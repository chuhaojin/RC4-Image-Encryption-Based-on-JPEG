#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : jpegFile.py
# @Time    : 2019/6/12 20:36
#@Software: PyCharm
import struct


# def write_jpeg(write_path, shape):
#     f = open(write_path, "wb")
#     f.close()
#     write_segment(app0_segment, write_path)
#     DQTy_segment = [0xff, 0xdb, 0x00, 0x43, 0x00] + [int(num) for Q in Qy for num in Q]
#     write_segment(DQTy_segment, write_path)
#     DQTc_segment = [0xff, 0xdb, 0x01, 0x43, 0x00] + [int(num) for Q in Qc for num in Q]
#     write_segment(DQTc_segment, write_path)
#
#     sof0_segment = [0xff, 0xc0, 0x00, 0x11, 0x08,
#                     shape[0]//256, shape[0] % 256, shape[1]//256, shape[1] % 256,
#                     0x03, 0x01, 0x22, 0x00, 0x02, 0x11, 0x01, 0x03, 0x11, 0x01]
#
#     write_segment(sof0_segment, write_path)
#     write_segment(HFMyDc_segment, write_path)
#     write_segment(HFMyAc_segment, write_path)
#     write_segment(HFMcDc_segment, write_path)
#     write_segment(HFMcAc_segment, write_path)
#     SOS_segment = [0xff, 0xda, 0x00, 0x0c, 0x03, 0x01, 0x00, 0x02, 0x11, 0x03, 0x11, 0x00, 0x3f, 0x00,
#                    0xe2, 0xe8, 0xa2, 0x8a, 0xf9, 0x93, 0xf7, 0x13]
#     write_segment(SOS_segment, write_path)
#     END_segment = [0xff, 0xd9]
#     write_segment(END_segment, write_path)
#     return

def get_stream(data, before_length):
    y_base = int(data[before_length + 4], base=2) * 65536 + int(data[before_length + 5], base=2) * 256
    length = y_base + int(data[before_length + 6], base=2)
    stream = "".join(data[before_length + 7: before_length + length])
    return stream, length + before_length

def read_jpeg(read_path):
    f = open(read_path, "rb")
    lines = f.readlines()
    data = [format(item, "#010b")[2:] for line in lines for item in line]
    shape0, shape1 = int(data[5] + data[6], base=2), int(data[7] + data[8], base=2)
    shape = (shape0, shape1, 3)
    head_length = int(data[4], base=2)
    before_length = head_length
    y_stream, before_length = get_stream(data, before_length)
    cb_stream, before_length = get_stream(data, before_length)
    cr_stream, _ = get_stream(data, before_length)
    return y_stream, cb_stream, cr_stream, shape


def get_seg(stream, id):
    padding = stream + '1' * ((8 - len(stream)) % 8)
    length = len(padding) // 8 + 7
    seg = [0xff, 0xff, 0xff, id, length//65536, (length % 65536)//256, length % 256]
    seg += [int(padding[i: i+8], base=2) for i in range(0, len(padding), 8)]
    return seg


def write_segment(segment, path):
    f = open(path, "ab")
    for info in segment:
        f.write(struct.pack('B', info))
    f.close()

def write_jpeg(write_path, y, cb, cr, shape):
    f = open(write_path, "wb")
    f.close()
    head_seg = [0xff, 0xff, 0xff, 0x00, 0x09, shape[0]//256, shape[0] % 256, shape[1]//256, shape[1] % 256]
    write_segment(head_seg, write_path)
    y_seg = get_seg(y, 0x01)
    write_segment(y_seg, write_path)
    cb_seg = get_seg(cb, 0x02)
    write_segment(cb_seg, write_path)
    cr_seg = get_seg(cr, 0x03)
    write_segment(cr_seg, write_path)


if __name__ == "__main__":
    import jpeg_encoder
    import jpeg_decoder
    in_path = "../data/test.jpg"
    read_path = write_path = "../data/output_test.jpeg"
    y, cb, cr = jpeg_encoder.jpeg_encode(in_path, write_path)
    y2, cb2, cr2, shape = read_jpeg(read_path)
    img = jpeg_decoder.jpeg_decode(read_path)

