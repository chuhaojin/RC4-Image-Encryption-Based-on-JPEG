#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : sequence.py
# @Time    : 2019/6/9 20:10
#@Software: PyCharm

from models.huffman import huffman_to_ldc, huffman_to_lac, huffman_encode
from models.huffman import ldc_to_huffman, lac_to_huffman

def sequence_encode(bit_list, dc_func, ac_func):
    huffman_list = huffman_encode(bit_list, dc_func=dc_func, ac_func=ac_func)
    return "".join([item[0] + item[1] for item in huffman_list])

def sequence_decode(sequence, dc_func, ac_func):
    huffman_list, result_list = [], []
    flag, dc_flag = 0, True
    while flag <= len(sequence):
        i, length = flag, 0
        while i <= len(sequence):
            if dc_flag:
                ratio = dc_func(sequence[flag: i])
                if ratio != None:
                    dc_flag, length = False, ratio
                    huffman_list.append((ratio, sequence[i: i + ratio]))
                    break
            else:
                ratio = ac_func(sequence[flag: i])
                if ratio != None:
                    length = int(ratio[1], base=16)
                    huffman_list.append((ratio, sequence[i: i + length]))
                    if ratio == "00":
                        result_list.append(huffman_list)
                        huffman_list, dc_flag = [], True
                    break
            i += 1
        flag = i + length
    return result_list


if __name__ == "__main__":
    test = [('1110', '100011'), ('100', '111'), ('111111110101', '001'), ('01', '01'),
            ('111111110100', '0110'), ('11111111001', ''), ('111111110100', '1000'), ('1010', '')]

    test2 = [(6, '100011'), ('03', '111'), ('33', '001'), ('02', '01'),
             ('24', '0110'), ('f0', ''), ('24', '1000'), ('00', '')]
    sequence = sequence_encode(test2, dc_func=ldc_to_huffman, ac_func=lac_to_huffman)
    print(test2)
    print(sequence)
    print(sequence_decode(sequence + sequence, dc_func=huffman_to_ldc, ac_func=huffman_to_lac)[1] == test2)
