#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : huffman.py
# @Time    : 2019/6/8 15:35
#@Software: PyCharm

from config import LDC_LIST, CDC_LIST, LAC_DICT, CAC_DICT

def get_inverse(table):
    inverse = {}
    if type(table) == list:
        for i in range(len(table)):
            inverse[table[i]] = i
        return inverse
    elif type(table) == dict:
        for item in table.items():
            inverse[item[1]] = item[0]
        return inverse
    return inverse

INVERSE_LDC_DICT = get_inverse(LDC_LIST)
INVERSE_CDC_DICT = get_inverse(CDC_LIST)
INVERSE_CAC_DICT = get_inverse(CAC_DICT)
INVERSE_LAC_DICT = get_inverse(LAC_DICT)
def num_to_huffman(num):
    if num > 0:
        return bin(num)[2:]
    elif num < 0:
        return bin(num - 1 & 4095)[-len(bin(abs(num))[2:]):]
    elif num == 0:
        return ''

def huffman_to_num(huffman_code):
    if len(huffman_code) == 0:
        return 0
    if huffman_code[0] == '1':
        return int(huffman_code, base=2)
    elif huffman_code[0] == '0':
        return -(~int(huffman_code, base=2) & int(len(huffman_code) * '1', base=2))

def ldc_to_huffman(ldc):
    return LDC_LIST[ldc]

def huffman_to_ldc(huffman_code):
    return INVERSE_LDC_DICT.get(huffman_code)

def cdc_to_huffman(cdc):
    return CDC_LIST[cdc]

def huffman_to_cdc(huffman_code):
    return INVERSE_CDC_DICT.get(huffman_code)

def lac_to_huffman(lac):
    return LAC_DICT[lac]

def huffman_to_lac(huffman_code):
    return INVERSE_LAC_DICT.get(huffman_code)

def cac_to_huffman(cac):
    return CAC_DICT[cac]

def huffman_to_cac(huffman_code):
    return INVERSE_CAC_DICT.get(huffman_code)

def huffman_encode(bit_list, dc_func, ac_func):
    huffman_list = []
    huffman_list.append((dc_func(bit_list[0][0]), bit_list[0][1]))
    for item in bit_list[1:]:
        huffman_list.append((ac_func(item[0]), item[1]))
    return huffman_list

def huffman_decode(huffman_list, dc_func, ac_func):
    bit_list = []
    bit_list.append((dc_func(huffman_list[0][0]), huffman_list[0][1]))
    for item in huffman_list[1:]:
        bit_list.append((ac_func(item[0]), item[1]))
    return bit_list


if __name__ == "__main__":
    huffman_code = num_to_huffman(0)
    print(huffman_code)
    num = huffman_to_num(huffman_code)
    print(num)
    hfm = ldc_to_huffman(len(huffman_code))
    print(hfm)
    dc = huffman_to_ldc(hfm)
    print(dc)
    bit_list = [(6, '100011'), ('03', '111'), ('33', '001'), ('02', '01'),
                ('24', '0110'), ('f0', ''), ('24', '1000'), ('00', '')]
    huffman_list = huffman_encode(bit_list, dc_func=ldc_to_huffman, ac_func=lac_to_huffman)
    print(huffman_list)
    temp = huffman_decode(huffman_list, dc_func=huffman_to_ldc, ac_func=huffman_to_lac)
    print(temp)
