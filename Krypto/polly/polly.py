import pwn
import re

# make files relative to script
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open('shadow', 'r') as f:
    user_hashes = f.read().split('\n')

with open("john.pot", "r") as f:
    hash_passwords = f.read().split('\n')

# remove lines which dont have 3 "$" signs then sort user_hashes by salt
user_hashes = [x for x in user_hashes if x.count('$') == 3]
user_hashes.sort(key=lambda x: x.split(':')[1])

hash_passwords = [x for x in hash_passwords if x.count('$') == 3]
hash_passwords.sort(key=lambda x: x.split(':')[0])

# john.pot already sorted by salt
passwd_dict = {}
j = 0
for i in range(len(hash_passwords)):
    while i+j < len(user_hashes) and user_hashes[i+j].split(":")[1].split('$')[3] != hash_passwords[i].split(':')[0].split('$')[3]:
        j += 1
    # print(user_hashes[i+j].split(":")[0], hash_passwords[i].split(':')[1])
    passwd_dict[user_hashes[i+j].split(":")[0]] = hash_passwords[i].split(':')[1]

host = "35.156.167.186"
port = 10003

def get_passwd(user, passwd_dict):
    if user in passwd_dict:
        return passwd_dict[user]
    return "nope"

io = pwn.connect(host, port)

correct = 0
while True:
    line = io.readline().decode()
    print(line)
    # search for regex ENO{[a-zA-Z0-9_]+}
    if re.search(r"ENO{[a-zA-Z0-9_]+}", line):
        break
    if "user" not in line:
        continue
    user = line.split()[-1][:-1]
    passwd = str(get_passwd(user, passwd_dict))
    if passwd != "nope":
        correct += 1
    io.sendline(passwd.encode())
print("Correct: ", correct)
print("Flag: ", line)