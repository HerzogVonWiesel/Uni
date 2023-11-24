#!/usr/bin/env python

from string import ascii_lowercase
from random import sample


def generate_random_key():
    return {k: v for (k, v) in zip(ascii_lowercase, sample(ascii_lowercase, len(ascii_lowercase)))}


def generate_key(password):
    assert all([c in ascii_lowercase for c in password])
    key = {}
    counter = 0
    for i in range(len(password)):
        if password[i] not in key:
            key[password[i]] = ascii_lowercase[counter]
            counter += 1
    for c in ascii_lowercase[::-1]:
        if c not in key:
            key[c] = ascii_lowercase[counter]
            counter += 1
    return key


def filter_text(text):
    return ''.join(filter(lambda c: c in ascii_lowercase, text.lower()))


def patristocrat(text):
    filtered_text = filter_text(text)
    return ' '.join([filtered_text[i:i + 5] for i in range(0, len(filtered_text), 5)])


def crypt(text, key, encrypt=True):
    if not encrypt:
        key = dict((v, k) for k, v in key.items())
    ciphertext = ''.join([key[c] if c in key else c for c in text.lower()])
    return ciphertext


def main():
    with open('solution/plaintext', 'r') as input_file:
        text = input_file.read().strip()
    with open('solution/flag', 'r') as input_file:
        flag = input_file.read().strip()
    with open('solution/password', 'r') as input_file:
        password = input_file.read().strip()
    plaintext = f'{text}\n{flag}'
    key = generate_key(password)
    # key = generate_random_key()
    formatted_plaintext = patristocrat(plaintext)
    ciphertext = crypt(formatted_plaintext, key)
    assert filter_text(plaintext) == filter_text(crypt(ciphertext, key, encrypt=False))
    with open('ciphertext.txt', 'w') as output_file:
        output_file.write(ciphertext + '\n')


if __name__ == '__main__':
    main()
