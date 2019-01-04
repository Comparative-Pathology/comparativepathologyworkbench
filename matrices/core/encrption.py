# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import urandom
from base64 import b64encode, b64decode
from django.db import models
from Crypto.Cipher import ARC4


def get_value(name):
    def f(self):
        return Password.decrypt(getattr(self, 'e_%s'%name))
    return f
    
def set_value(name):
    def f(self, value):
        setattr(self, 'e_%s'%name, Password.encrypt(value))
    return f
    

class Password(models.Model):
    SALT_SIZE = 8
    
    name = models.CharField(max_length=128)
    #slug = models.SlugField()
    e_username = models.TextField(blank=True)
    e_password = models.TextField(blank=True)
    #e_host = models.TextField(blank=True)
    #e_resource = models.TextField(blank=True)

    @staticmethod
    def encrypt(plaintext):
        salt = urandom(Password.SALT_SIZE)
        arc4 = ARC4.new(salt + settings.SECRET_KEY)
        plaintext = "%3d%s%s" % (len(plaintext), plaintext, urandom(256-len(plaintext)))
        return "%s$%s" % (b64encode(salt), b64encode(arc4.encrypt(plaintext)))
        
    @staticmethod
    def decrypt(ciphertext):
        salt, ciphertext = map(b64decode, ciphertext.split('$'))
        arc4 = ARC4.new(salt + settings.SECRET_KEY)
        plaintext = arc4.decrypt(ciphertext)
        return plaintext[3:3+int(plaintext[:3].strip())]
    
    def encrypted_property(name):
        return property(get_value(name), set_value(name))    
    

    username = encrypted_property('username')
    password = encrypted_property('password')
    #host = encrypted_property('host')
    #resource = encrypted_property('resource')
