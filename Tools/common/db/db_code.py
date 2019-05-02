# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/9/1

#加解密password方法
# code_al = AES.new('SpiderWonder Enc', AES.MODE_CBC, 'SpiderWonder Enc')


import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class Code_A():
    def __init__(self):
        self.key = 'SpiderWonder Enc'
        self.mode = AES.MODE_CBC

    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

code_al = Code_A()

if __name__ =='__main__':
    str = 'asdfa'
    length = 16
    count = len(str)
    add = length - (count % length)
    text = str + ('\0' * add)
    # val =b2a_hex(code_al.encrypt(text))
    val =code_al.encrypt(text)
    print(val)
    # print a2b_hex(text)
    # print code_al.decrypt(a2b_hex(text)).rstrip('\0')
    # print code_al.decrypt(text).rstrip('\0')
    # #pc = prpcrypt('SpiderWonder Enc')      #初始化密钥
    # e = code_al.encrypt("00000")
    # d = code_al.decrypt(e)
    # print e, d
    # e = code_al.encrypt("0000000000000000000000000")
    # d = code_al.decrypt(e)
    # print e, d