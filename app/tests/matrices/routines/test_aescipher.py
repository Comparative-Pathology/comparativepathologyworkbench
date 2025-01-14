import unittest
from matrices.routines.aescipher import AESCipher


class TestAESCipher(unittest.TestCase):

    def setUp(self):
        self.key = "mysecretpassword"
        self.cipher = AESCipher(self.key)

    def test_encrypt_decrypt(self):
        plaintext = "This is a test message."
        encrypted = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(encrypted).decode('utf-8')
        self.assertEqual(plaintext, decrypted)

    def test_encrypt_not_equal_plaintext(self):
        plaintext = "This is a test message."
        encrypted = self.cipher.encrypt(plaintext)
        self.assertNotEqual(plaintext, encrypted)

    def test_decrypt_invalid_data(self):
        with self.assertRaises(ValueError):
            self.cipher.decrypt(b"invalid data")


if __name__ == '__main__':
    unittest.main()
# The test case above is a unit test for the AESCipher class. It tests the encryption and decryption methods of the class. 
# It uses a fixed key and plaintext message to verify the correctness of the encryption and decryption process. 
# It also tests the handling of invalid data during decryption.