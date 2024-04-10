#!/usr/bin/env python3
import os
import sys
from Crypto.Cipher import AES
from Crypto.Util import Counter
from binascii import hexlify

def log(*err_messages):
	'''function for debugging purposes'''
	logs = open('err.log','a')
	for msg in err_messages:
		if type(msg) == bytes: msg = hexlify(msg).decode()
		logs.write(msg)
	logs.write('\n')
	logs.close()

def enc(msg : bytes, key : bytes) -> bytes:
	'''Encrypt message with AES'''
	aes = AES.new(key, AES.MODE_CTR, counter = Counter.new(128,initial_value = 0))
	return aes.encrypt(msg)

dec = enc #corresponding decryption function

def encrypt(msg, key : bytes):
	'''Encrypt message with ONe-Time-Pad'''
	if type(msg) == str: msg = msg.encode()
	return hexlify(bytes([msg[i] ^ key[i % 32] for i in range(len(msg))])).decode()

if __name__ == '__main__':
	try:
		flag = open('flag','r').read().strip()
		key = os.urandom(32)
		cipher = enc(flag.encode(), key)
		print(hexlify(cipher).decode())
		log('cipher: ', cipher)
		log('key: ', key)
		print('I will encrypt a single message of length at most 30 for you.\nMessage: ')
		sys.stdout.flush()
		message = sys.stdin.buffer.readline().strip()
		assert len(message) <= 30
		print(encrypt(message, key))
	except Exception as err:
		print('Something went wrong')
		log('ERROR: ', repr(err))
