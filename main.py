#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author  : Chuhao Jin
# @Email   : chuhao.j@gmail.com
# @File    : main.py
# @Time    : 2019/6/14 14:15
#@Software: PyCharm

import decryption, encryption, jpeg_decoder, jpeg_encoder

def action(option):
    if option == 1:
        read_path = input("要读取的图片路径：")
        write_path = input("写文件路径：")
        jpeg_encoder.jpeg_encode(read_path, write_path)
        print("文件压缩成功！")
    elif option == 2:
        read_path = input("要读取的图片路径：")
        jpeg_decoder.jpeg_decode(read_path)
    elif option == 3:
        read_path = input("要读取的图片路径：")
        write_path = input("写文件路径：")
        key = input("输入密钥：")
        en_rank = int(input("输入加密等级（1~8）："))
        encryption.jpeg_encryption(read_path, write_path, key, en_rank)
        print("文件加密成功！")
    elif option == 4:
        read_path = input("要解密的图片路径：")
        key = input("输入密钥：")
        en_rank = int(input("输入加密等级（1~8）："))
        decryption.jpeg_decryption(read_path, key, en_rank)
    return


if __name__ == "__main__":
    print("*" * 50)
    print("可选项如下：")
    print("\t1.图像压缩")
    print("\t2.图像展示")
    print("\t3.图像加密")
    print("\t4.图像解密")
    print("\t5.退出")
    while True:
        try:
            option = int(input("请输入您的选项（1：压缩 2：展示 3：加密 4：解密 5:退出）："))
            if option == 5:
                break
            if option < 1 or option > 4:
                raise TypeError
            else:
                action(option)
        except:
            print("输入不合法，请重新输入！")

