from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes

# make files relative to script
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def save_flag():
	flag = open('flag','r').read().strip().encode()
	flag = bytes_to_long(flag)

	n = 1
	output = open('output','w')
	while n < flag:
		p = getPrime(64)
		output.write('%d,%d\n' % (flag % p, p))
		n *= p
	output.close()

def EEA(a, b):
	if b == 0:
		return (a, 1, 0)
	d, s, t = EEA(b, a % b)
	return (d, t, s - (a // b) * t)

def retrieve_flag():
	output = open('output','r')
	flag = 1
	ar = []
	pr = []
	for line in output:
		x, y = line.strip().split(',')
		ar.append(int(x))
		pr.append(int(y))
	
	a_p = ar[0]
	p_p = pr[0]
	for a, p in zip(ar[1:], pr[1:]):
		d, s, t = EEA(p_p, p)
		print(d, s, t)
		a_p = a_p * t * p + a * s * p_p
		p_p *= p
	
	flag = long_to_bytes(a_p % p_p)
	print(flag.decode())

retrieve_flag()
