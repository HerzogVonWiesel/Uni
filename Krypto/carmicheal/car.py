def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def isprime(n):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for a in range(3, n, 2):
        if n % a == 0:
            return False
    return True

print("Carmicheal numbers:")
for n in range(2, 2000):
    for a in range(1, n):
        if gcd(a, n) != 1:
            continue
        if pow(a, n-1) % n != 1:
            break
    else:
        if not isprime(n):
            print(n)