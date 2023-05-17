#!/usr/bin/python3
###!
# \file         aescipher.py
# \author       Mike Wicks
# \date         March 2021
# \version      $Id$
# \par
# (C) University of Edinburgh, Edinburgh, UK
# (C) Heriot-Watt University, Edinburgh, UK
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
# \brief
# AES Cipher for Encryption and Decryption
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom

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

        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )

        encoded = base64.b64encode( iv + cipher.encrypt( raw.encode('utf8') ) )

        return encoded


    def decrypt( self, enc ):

        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )

        decoded = unpad(cipher.decrypt( enc[16:] ))

        return decoded
