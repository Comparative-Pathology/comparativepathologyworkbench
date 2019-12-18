# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import urandom

import base64, hashlib

from Crypto.Cipher import AES
from Crypto import Random


"""
    Lambda functions for Padding and Unpadding
"""
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]


"""
    AES Cipher Class
"""
class AESCipher:

    def __init__( self, key ):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()


    def encrypt( self, raw ):

        print("raw : ", raw)

        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )

        encoded = base64.b64encode( iv + cipher.encrypt( raw.encode('utf8') ) )

        print("encoded : ", encoded)

        return encoded


    def decrypt( self, enc ):

        print("enc : ", enc)

        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )

        decoded = unpad(cipher.decrypt( enc[16:] ))

        print("decoded : ", decoded)

        return decoded
