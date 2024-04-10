#!/usr/bin/env python3
import random
import signal
import sys

class TimeoutError(Exception):
	"""Basic Error class for timeouts."""

	pass

class timeout:
	"""Small environment to impose a maximum time for commands."""

	def __init__(self, seconds=1, error_message='Timeout'):
		"""Setup the timer with the given amount of seconds."""
		self.seconds = seconds
		self.error_message = error_message
	def handle_timeout(self, signum, frame):
		"""Event that happens, if the maximal time is reached."""
		raise TimeoutError(self.error_message)
	def __enter__(self):
		"""Start the timer, when entering the environment."""
		signal.signal(signal.SIGALRM, self.handle_timeout)
		signal.alarm(self.seconds)
	def __exit__(self, type, value, traceback):
		"""Stop the timer, when leaving the environment."""
		signal.alarm(0)

N = 256
ratio = 0.5

solutions = [(x[1],x[4]) for x in [line.split(' ') for line in open('shadow-lsg','r').read().splitlines()]]

def loop():
	counter = 0
	for _ in range(N):
		with timeout(1):
			user, password = random.choice(solutions)
			print(f'Give password for user {user}:')
			sys.stdout.flush()
			pw = sys.stdin.buffer.readline().strip()
			if type(pw) == bytes: pw = pw.decode()
			if pw == password: 
				print('okay')
				counter += 1
			else:
				print('wrong')
	return counter

if __name__ == '__main__':
	try:
		counter = loop()
		if counter > N * ratio:
			print(open('flag','r').read().strip())
		else:
			print(f'Not enough correct passwords: {counter} out of {N}')
	except Exception as err:
		print(repr(err))
		print('Error')
