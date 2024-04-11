#!/usr/bin/env python3
import os
import sys
import string
from Crypto.Util import number
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from binascii import hexlify

from ec import *
from utils import *
#from secret import flag1, flag2

#P-256 parameters
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
curve = EllipticCurve(p,a,b, order = n)
G = ECPoint(curve, 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

d_a = bytes_to_long(os.urandom(32))
P_a = G * d_a

printable = [ord(char.encode()) for char in string.printable]

def encrypt(msg : bytes, pubkey : ECPoint):
	x = bytes_to_long(msg)
	y = modular_sqrt(x**3 + a*x + b, p)
	m = ECPoint(curve, x, y)
	d_b = number.getRandomRange(0,n)
	return (G * d_b, m + (pubkey * d_b))

def decrypt(B : ECPoint, c : ECPoint, d_a : int):
	if B.inf or c.inf: return b''
	return long_to_bytes((c - (B * d_a)).x)

def loop():
	print('I will decrypt anythin as long as it does not talk about flags.')
	balance = 1024
	while True:
		print('B:', end = '')
		sys.stdout.flush()
		B_input = sys.stdin.buffer.readline().strip().decode()
		print('c:', end = '')
		sys.stdout.flush()
		c_input = sys.stdin.buffer.readline().strip().decode()
		B = ECPoint(curve, *[int(_) for _ in B_input.split(',')])
		c = ECPoint(curve, *[int(_) for _ in c_input.split(',')])
		msg = decrypt(B, c, d_a)
		if b'ENO' in msg:
			balance = -1
		else:
			balance -= 1 + len([c for c in msg if c in printable])
		if balance >= 0:
			print(hexlify(msg))
			print('balance left: %d' % balance)
		else:
			print('You cannot afford any more decryptions.')
			return


import pwn
if __name__ == '__main__':
	host = "ctffb24.hpi.de"
	port = 10012
	io = pwn.connect(host, port)
	io.readline().decode()
	public_A = io.readline().decode()
	io.readline().decode()
	given_B = io.readline().decode()
	given_c = io.readline().decode()
	io.readline().decode()
	io.readline().decode()
	
	# make string "Point(13, 21)" into "13, 21"
	public_A = public_A[6:-2]
	given_B = given_B[6:-2]
	given_c = given_c[6:-2]
	given_c_x = given_c.split(', ')[0]
	given_c_y = given_c.split(', ')[1]

	given_c_y = int(given_c_y) + 1

	io.sendline(given_B)
	io.sendline(str(given_c_x) + ", " + str(given_c_y))
	bytemsg = io.readline()[4:].decode()
	print(bytemsg)
	x = bytes_to_long(bytemsg)
	y = modular_sqrt(x**3 + a*x + b, p) - 1
	ECPoint
	print(io.readline().decode())


def oldmain():
	print('My public key is:')
	print(P_a)
	print('Good luck decrypting this cipher.')
	B,c = encrypt(flag1, P_a)
	print(B)
	print(c)
	key = long_to_bytes((d_a >> (8*16)) ^ (d_a & 0xffffffffffffffffffffffffffffffff))
	enc = AES.new(key, AES.MODE_ECB)
	cipher = enc.encrypt(flag2)
	print(hexlify(cipher).decode())
	try:
		loop()
	except Exception as err:
		print(repr(err))
