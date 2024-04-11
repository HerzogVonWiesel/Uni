#!/usr/bin/python3
import random
from Crypto.Cipher import AES
from hashlib import sha256
# from secret import flag, generate_base
import os
import sympy

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class Permutation(object):
	def __init__(self, perm):
		self.perm = perm.copy()
		self.n = len(perm)
	
	def __mul__(self, perm):
		if self.n != perm.n:
			raise Exception
		return Permutation([perm.perm[self.perm[i]] for i in range(self.n)])

	def __str__(self):
		return str(self.perm)

	def to_key(self):
		b = 1
		while 256**b <= self.n:
			b += 1
		res = b''
		for x in self.perm:
			res += x.to_bytes(b,'big')
		return sha256(res).digest()

def pow(perm, k):
	if type(perm) == list: perm = Permutation(perm)
	res = Permutation(list(range(perm.n)))
	x = Permutation(perm.perm)
	if k == 0: return res
	while k > 1:
		if k & 1:
			res = x * res
		x = x * x
		k >>= 1
	return x * res

def write_flag():
	p = generate_base(1<<16)
	a = random.randint(0, 1<<256)
	b = random.randint(0, 1<<256)
	A = pow(p,a)
	B = pow(p,b)
	writer = open('output','w')
	writer.write('p = %s\nA = %s\nB = %s\n' % (str(p), str(A), str(B)))
	key_Alice = pow(A,b).to_key()
	key_Bob = pow(B,a).to_key()
	assert key_Alice == key_Bob
	cipher = AES.new(key_Alice, AES.MODE_CBC, bytes(16))
	code = cipher.encrypt(flag.encode() + b'\x00' * (16 - len(flag) % 16))
	writer.write('enc_flag = %s' % code.hex())
	writer.close()

def to_cycles(perm):
    pi = {i: perm[i] for i in range(len(perm))}
    cycles = []
    while pi:
        elem0 = next(iter(pi)) # arbitrary starting element
        this_elem = pi[elem0]
        next_item = pi[this_elem]
        cycle = []
        while True:
            cycle.append(this_elem)
            del pi[this_elem]
            this_elem = next_item
            if next_item in pi:
                next_item = pi[next_item]
            else:
                break
		# move last element to first
        cycle = cycle[-1:] + cycle[:-1]
        cycles.append(cycle)
    return cycles

def get_cycle_system(cycle_1, cycle_2):
	m = []
	v = []
	for elem_1, elem_2 in zip(cycle_1, cycle_2):
		if len(elem_1) > 1:
			found = False
			m.append(len(elem_1))
			for i in range(1, len(elem_1)):
				if elem_2[1] == elem_1[i]:
					v.append(i)
					found = True
					break
			if not found:
				print('Error: cycle_1 and cycle_2 are not compatible')

	return m, v
		

def decode_flag():
	with open('output','r') as input_file:
		text = input_file.read().strip()
		p = text.split('\n')[0].split(' = ')[1]
		A = text.split('\n')[1].split(' = ')[1]
		B = text.split('\n')[2].split(' = ')[1]
		enc_flag = text.split('\n')[3].split(' = ')[1]
		print("---\n%s\n---" % enc_flag)
		# print('p = %s\nA = %s\nB = %s\nenc_flag = %s\n' % (str(p), str(A), str(B), str(enc_flag)))
		# p to list, A to list, B to list
		p = list(map(int, p[1:-1].split(', ')))
		A = list(map(int, A[1:-1].split(', ')))
		B = list(map(int, B[1:-1].split(', ')))
		enc_flag = bytes.fromhex(enc_flag)
		print("---\n%s\n---" % enc_flag)
		# print('p = %s\nA = %s\nB = %s\nenc_flag = %s\n' % (str(p), str(A), str(B), str(enc_flag)))
		p = Permutation(p)
		A = Permutation(A)
		B = Permutation(B)
		p_c = to_cycles(p.perm)
		A_c = to_cycles(A.perm)
		B_c = to_cycles(B.perm)
		m, v = get_cycle_system(p_c, A_c)
		a, a_mod = sympy.ntheory.modular.crt(m, v)
		print(a)
		print(a_mod)
		key_Eve = pow(B,a).to_key()
		cipher = AES.new(key_Eve, AES.MODE_CBC, bytes(16))
		dec_flag = cipher.decrypt(enc_flag)
		print(dec_flag)
		print(dec_flag.decode())

		

# print(to_cycles([1,2,6,5,0,3,4]))
# cyc_p = [[1, 7], [2, 6, 8], [3, 5, 4, 9, 10]]
# cyc_a = [[1, 7], [2, 8, 6], [3, 4, 10, 5, 9]]
# m, v = get_cycle_system(cyc_p, cyc_a)
# print(m, v)
# print(sympy.ntheory.modular.crt(m, v)[0])
decode_flag()