#!/usr/bin/env python3

from Crypto.Cipher import AES
import os, sys
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def encrypt(img_in):
    img_in += b'\00' * (16 - (len(img_in) % 16))
    cipher = AES.new(os.urandom(16), AES.MODE_ECB)
    img_out = cipher.encrypt(img_in)
    return img_out

def _remove_padding(data):
	pad_len = data[-1]
	
	if pad_len < 1 or pad_len > 16:
		return None
	for i in range(1, pad_len):
		if data[-i-1] != pad_len:
			return None
	return data[:-pad_len]

def _decrypt(data):
	iv = data[:16]
	cipher = AES.new(os.urandom(16), AES.MODE_ECB)
	return _remove_padding(cipher.decrypt(data[16:]))


def is_padding_ok(data):
	return _decrypt(data) is not None

def decrypt(img_in, key):
    cipher = AES.new(key, AES.MODE_ECB)
    img_out = cipher.decrypt(img_in)
    return img_out

def find_padding_length(ciphertext):
    for i in range(1, 17):
        modified_ciphertext = bytearray(ciphertext)
        modified_ciphertext[-i] ^= 1  # guess the padding value
        try:
            decrypt(modified_ciphertext, os.urandom(16))
        except ValueError:
            # Padding error occurred, so the guessed padding length is correct
            return i
    print("Couldn't find padding length")

def check_padding(img_in):
    cipher = AES.new(os.urandom(16), AES.MODE_ECB)
    img_out = cipher.decrypt(img_in)
    return img_out

with open('flag.bmp', 'rb') as input_file:
    img_in = input_file.read()
    # save 16 versions of the ciphertext, removing 1 byte at a time
    for i in range(1, 17):
        with open(str(i) + 'flag.bmp', 'wb') as output_file:
            output_file.write(img_in[:-i])