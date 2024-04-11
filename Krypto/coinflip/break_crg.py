import os
import sys
from Crypto.Util.number import bytes_to_long, getRandomNBitInteger
import math

import pwn
import re

host = "ctffb24.hpi.de"
port = 10010
io = pwn.connect(host, port)


class CRG(object):
	"""Cubic Random Generator"""

	def __init__(self, n):
		'''n - bitlength of state'''
		self.n = n
		self.m = getRandomNBitInteger(n)
		while True:
			self.a = bytes_to_long(os.urandom(n >> 3)) % self.m # n/8 bytes 8
			if math.gcd(self.a, self.m) == 1: break
		while True:
			self.state = bytes_to_long(os.urandom(n >> 3)) % self.m # n/8 bytes 8
			if math.gcd(self.state, self.m) == 1: break
		self.buffer = []

	def next(self):
		if self.buffer == []:
			self.buffer = [int(bit) for bit in bin(self.state)[2:].zfill(self.n)]
			self.state = self.a * pow(self.state, 3, self.m) % self.m
			#log('new state: ', self.state)
		return self.buffer.pop(0)
	

# buffer always starts with 00
class BreakCRG():
    def __init__(self, n):
        self.n = n
        self.cur_y = "0b"
        self.y_k_minus_1 = None
        self.y_k = None
        self.y_k_plus_1 = None

        self.u = []

    def get_next_bit(self):
        io.readline().decode()
        io.sendline("1".encode())
        io.readline().decode()
        io.sendline("head".encode())
        if "win" in io.readline().decode():
            return 0
        else:
            return 1
		
    def get_next_y(self):
        for i in range(self.n):
            bit = self.get_next_bit()
            self.cur_y += str(bit)
        self.y_k_minus_1 = self.y_k
        self.y_k = self.y_k_plus_1
        self.y_k_plus_1 = int(self.cur_y, 0)
        print("y_k_minus_1: ", self.y_k_minus_1)
        print("y_k: ", self.y_k)
        print("y_k_plus_1: ", self.y_k_plus_1)
        self.cur_y = "0b"

    def get_next_u(self):
        if self.y_k_minus_1 == None:
            self.get_next_y()
            self.get_next_y()
            self.get_next_y()
        else:
            self.get_next_y()
            self.u.append(self.y_k_plus_1 * pow(self.y_k_minus_1, 3) - pow(self.y_k, 4))

    def calculate_m(self):
        m = math.gcd(*self.u[1:])
        return int(m)
    
    def calculate_a(self, m):
        a = (self.y_k_plus_1 *pow(pow(self.y_k, 3, m), -1, m)) % m
        return int(a)
    
    def calculate_state(self, m, a):
        state = (a * pow(self.y_k_plus_1, 3, m)) % m
        return int(state)
    
    def win_game(self):
        for i in range(10):
            self.get_next_u()
        print("u: ", self.u)
        m = self.calculate_m()
        a = self.calculate_a(m)
        state = self.calculate_state(m, a)
        print("m: ", m)
        print("a: ", a)
        print("state: ", state)
        buffer = [int(bit) for bit in bin(state)[2:].zfill(self.n)]
        while True:
            line = io.readline().decode()
            if re.search(r"ENO{[a-zA-Z0-9_]+}", line):
                break
            money = line.split()[-1][:-1]
            print(money)
            io.sendline(money.encode())
            io.readline().decode()
            print()
            if buffer.pop(0) == 0:
                io.sendline("head".encode())
            else:
                io.sendline("tails".encode())
            print(io.readline().decode())
        print("Flag: ", line)
         

break_crg = BreakCRG(64)
break_crg.win_game()
		
    
		
