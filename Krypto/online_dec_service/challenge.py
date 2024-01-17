#!/usr/bin/env python

from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES256
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.hashes import SHA3_512
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.exceptions import InvalidSignature
import secrets
import base64
import binascii


WELCOME_MESSAGE = 'Welcome to the online encryption service!'
COMMAND_EXPLANATION = '''
Plaintext and ciphertext must (input) and will be (output) base64 encoded! Inputs must be and outputs will be terminated with a newline. You can execute the following commands:
\tencrypt <plaintext>   -> <ciphertext>     (result of the encryption)
\tvalidate <ciphertext> -> <status>         (text describing whether ciphertext is valid or not)
\texample               -> <ciphertext>     (example encryption result that you can validate)
\tsource                -> <__file__>       (server\'s python code)'''
PROMPT = '> '


class AES:
    def __init__(self):
        prp_key = secrets.token_bytes(AES256.key_size // 8)
        self.prp = AES256(prp_key)
        mac_key = secrets.token_bytes(SHA3_512.digest_size // 8)
        self.mac = HMAC(mac_key, SHA3_512())

    def calculate_mac(self, message):
        mac = self.mac.copy()
        mac.update(message)
        return mac.finalize()

    def encrypt(self, plaintext):
        iv = secrets.token_bytes(self.prp.block_size // 8)
        encryptor = Cipher(self.prp, CBC(iv)).encryptor()
        padder = PKCS7(self.prp.block_size).padder()
        padded_plaintext = padder.update(plaintext) + padder.finalize()
        return iv + encryptor.update(padded_plaintext) + encryptor.finalize()

    def encrypt_authenticated(self, message):
        return self.encrypt(message + self.calculate_mac(message))

    def decrypt(self, ciphertext):
        iv = ciphertext[:self.prp.block_size // 8]
        ciphertext = ciphertext[self.prp.block_size // 8:]
        decryptor = Cipher(self.prp, CBC(iv)).decryptor()
        unpadder = PKCS7(self.prp.block_size).unpadder()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return unpadder.update(padded_plaintext) + unpadder.finalize()

    def decrypt_verify(self, ciphertext):
        plaintext = self.decrypt(ciphertext)
        message = plaintext[:-self.mac.algorithm.digest_size]
        digest = plaintext[-self.mac.algorithm.digest_size:]
        mac = self.mac.copy()
        mac.update(message)
        mac.verify(digest)
        return message


def main():
    print(WELCOME_MESSAGE)
    aes_instance = AES()
    with open('flag', 'r') as flag_file:
        flag = flag_file.read().strip()
    if not flag:
        print('No flag set. Quitting...')
        exit(1)
    assert aes_instance.decrypt_verify(aes_instance.encrypt_authenticated(b'test')) == b'test'

    while True:
        print(COMMAND_EXPLANATION)
        user_input = input(PROMPT).strip().split()
        match user_input:
            case ['source']:
                with open(__file__, 'r') as current_file:
                    print(current_file.read())
            case ['example']:
                ciphertext = aes_instance.encrypt_authenticated(b'Here is a flag: ' + flag.encode())
                print(base64.b64encode(ciphertext).decode())
            case ['encrypt', plaintext]:
                try:
                    ciphertext = aes_instance.encrypt_authenticated(base64.b64decode(plaintext))
                    print(base64.b64encode(ciphertext).decode())
                except binascii.Error:
                    print('Invalid base64.')
            case ['validate', ciphertext]:
                try:
                    aes_instance.decrypt_verify(base64.b64decode(ciphertext))
                    print('Ciphertext is valid.')
                except binascii.Error:
                    print('Invalid base64.')
                except (InvalidSignature, ValueError) as e:
                    print(f'Ciphertext is invalid: {e}')
            case _:
                print('Unknown command.')


if __name__ == '__main__':
    main()
