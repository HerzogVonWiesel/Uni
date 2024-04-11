import pwn

host = "challenge.training.enoflag.de"
port = 10010

def find_next_prime(num):
    while True:
        num += 1
        for i in range(2, num):
            if num % i == 0:
                break
        else:
            return num

io = pwn.connect(host, port)

while True:
    line = io.readline().decode()
    print(line)
    if "Level" not in line:
        continue
    number = int(line.split()[-1][:-1])
    print(number)
    io.write(str(find_next_prime(number)))