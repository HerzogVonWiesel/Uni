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

import pwn
import re

from itertools import cycle

host = "ctffb24.hpi.de"
port = 10011
io = pwn.connect(host, port)

def base64_to_bytes(s):
    return base64.b64decode(s)

def bytes_to_base64(b):
    return base64.b64encode(b)

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
    
class CBC_BRK:
    def __init__(self, oracle_io):
        self.blocksize = 16
        self.oracle_io = oracle_io

    def set_ciphertext(self, ciphertext):
        self.ciphertext = ciphertext

    def skip_text(self):
        self.oracle_io.recvuntil("\n>".encode())

    def encrypt(self, plaintext):
        self.skip_text()
        text = "encrypt "+plaintext
        io.sendline(text.encode())
        return io.readline().decode().strip().encode()
    
    def validate(self, ciphertext):
        self.skip_text()
        text = "validate ".encode()+ciphertext
        io.sendline(text)
        line = io.readline().decode()
        # print(text)
        # print(line)
        return "Invalid padding" not in line

    def get_flag(self):
        self.skip_text()
        io.sendline("example".encode())
        return base64.b64decode(io.readline().decode().strip().encode())

    def test_validity(self, response):
        response_bytes_from_hex = bytes.fromhex(response)
        response_bytes_from_hex = base64.b64encode(response_bytes_from_hex)
        return self.validate(response_bytes_from_hex)

    def split_len(self, seq, length):
        return [seq[i : i + length] for i in range(0, len(seq), length)]

    """ Create custom block for the byte we search"""
    def block_search_byte(self, size_block, i, pos, l):
        hex_char = hex(pos).split("0x")[1]
        return (
            "00" * (size_block - (i + 1))
            + ("0" if len(hex_char) % 2 != 0 else "")
            + hex_char
            + "".join(l)
        )

    """ Create custom block for the padding"""
    def block_padding(self, size_block, i):
        l = []
        for t in range(0, i + 1):
            l.append(
                ("0" if len(hex(i + 1).split("0x")[1]) % 2 != 0 else "")
                + (hex(i + 1).split("0x")[1])
            )
        return "00" * (size_block - (i + 1)) + "".join(l)

    def hex_xor(self, s1, s2):
        b = bytearray()
        for c1, c2 in zip(bytes.fromhex(s1), cycle(bytes.fromhex(s2))):
            b.append(c1 ^ c2)
        return b.hex()

    def run(self, cipher):
        cipher = cipher.upper()
        size_block = self.block_size
        found = False
        valide_value = []
        result = []
        len_block = size_block * 2
        cipher_block = self.split_len(cipher, len_block)

        # for each cipher_block
        for block in reversed(range(1, len(cipher_block))):
            if len(cipher_block[block]) != len_block:
                print("[-] Abort length block doesn't match the size_block")
                break
            print("[+] Search value block : ", block, "\n")
            # for each byte of the block
            for i in range(0, size_block):
                # test each byte max 255
                for ct_pos in range(0, 256):
                    # 1 xor 1 = 0 or valide padding need to be checked
                    if ct_pos != i + 1 or (
                        len(valide_value) > 0 and int(valide_value[-1], 16) == ct_pos):

                        bk = self.block_search_byte(size_block, i, ct_pos, valide_value)
                        bp = cipher_block[block - 1]
                        bc = self.block_padding(size_block, i)

                        tmp = self.hex_xor(bk, bp)
                        cb = self.hex_xor(tmp, bc).upper()

                        up_cipher = cb + cipher_block[block]
                        # time.sleep(0.5)

                        if self.test_validity(up_cipher):
                            found = True

                            # data analyse and insert in right order
                            value = re.findall("..", bk)
                            valide_value.insert(0, value[size_block - (i + 1)])

                            bytes_found = "".join(valide_value)
                            if (
                                i == 0
                                and int(bytes_found, 16) > size_block
                                and block == len(cipher_block) - 1
                            ):
                                print(
                                    "[-] Error decryption failed the padding is > "
                                    + str(size_block)
                                )

                            print(
                                "\033[36m" + "\033[1m" + "[+]" + "\033[0m" + " Found",
                                i + 1,
                                "bytes :",
                                bytes_found,
                            )

                            break
                if found == False:
                    # lets say padding is 01 for the last byte of the last block (the padding block)
                    if len(cipher_block) - 1 == block and i == 0:
                        value = re.findall("..", bk)
                        valide_value.insert(0, "01")
                    else:
                        print("\n[-] Error decryption failed")
                        result.insert(0, "".join(valide_value))
                        hex_r = "".join(result)
                        print("[+] Partial Decrypted value (HEX):", hex_r.upper())
                        padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
                        print(
                            "[+] Partial Decrypted value (ASCII):",
                            bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),
                        )
                found = False

            result.insert(0, "".join(valide_value))
            valide_value = []

        print("")
        hex_r = "".join(result)
        print("[+] Decrypted value (HEX):", hex_r.upper())
        padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
        print(
            "[+] Decrypted value (ASCII):",
            bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),
        )

    def has_valid_padding(self, ciphertext: bytes) -> bool:
        return self.validate(base64.b64encode(ciphertext))

    def find_c_prime_at_index(self, ciphertext: bytearray, index: int):
        if not isinstance(ciphertext, bytearray):
            print(f"ciphertext not an instance of {bytearray}")

        # Replace ciphertext at index with a guessed byte
        ciphertext_temp = ciphertext
        for c_prime in range(256):
            ciphertext_temp[index] = c_prime
            if self.has_valid_padding(ciphertext_temp):
                return c_prime

        print(f"No valid padding found, is .has_valid_padding(...) implemented correctly?")

    def decrypt_block(self, c_i):
        if not isinstance(c_i, bytearray):
            print(f"block c_i not an instance of {bytearray}")

        c_previous = bytearray(b"\x00" * self.blocksize)
        intermediate = bytearray(b"\x00" * self.blocksize)

        for i in range(self.blocksize):
            self.progress_bar(i, self.blocksize - 1, "Decrypting ")
            for j in range(i):
                c_previous[(self.blocksize - 1) - j] = intermediate[(self.blocksize - 1) - j] ^ (i + 1)

            c_prime = self.find_c_prime_at_index(c_previous + c_i, (self.blocksize - 1) - i)
            intermediate[(self.blocksize - 1) - i] = c_prime ^ (i + 1)
            print(f"intermediate: {[hex(x)[2:] for x in intermediate]}")
        return intermediate

    def get_intermediate(self, ciphertext) -> bytes:
        key = b""
        blocks = len(ciphertext) // self.blocksize

        # Iterate blocks last to first
        for i in range(blocks):
            block_start = len(ciphertext) - (i + 1) * self.blocksize
            block_end = len(ciphertext) - (i * self.blocksize)
            key = self.decrypt_block(ciphertext[block_start:block_end]) + key
        return key

    def decrypt(self) -> bytes:
        print(f"Ciphertext length: {len(self.ciphertext)}")
        print(f"Blocks to decrypt: {len(self.ciphertext) // self.blocksize}")

        # Convert self.ciphertext to mutable bytearray
        self.ciphertext = bytearray(self.ciphertext)

        key = self.get_intermediate(self.ciphertext)
        plaintext = bytearray()

        for i in range(len(self.ciphertext) - self.blocksize):
            b = self.ciphertext[i] ^ key[i + self.blocksize]
            plaintext += (b).to_bytes(1, byteorder="big")
        print("\n")  # print variable on new line from progress bar
        return plaintext

    def progress_bar(self, i, total_length, post_text):
        n_bar = 100  # size of progress bar
        j = i / total_length
        print("\r")
        print(f"[{'#' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {post_text}")
        print()

break_cbc = CBC_BRK(io)
break_cbc.set_ciphertext(break_cbc.get_flag())
print(break_cbc.decrypt())