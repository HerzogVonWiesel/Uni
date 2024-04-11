from sage.all import *

n= 30030

def decrypt():
    P = PolynomialRing(Zmod(n), 'x', implementation='NTL')
    (x,) = P._first_ngens(1)
    for m_length in range(0, 8*18):
        invo = pow(1921984, -1, n)
        print(invo)
        f = x**3 + (1911984*invo)*x**2 + (754428*invo)*x + (119194*invo)
        m = f.small_roots()
        if m:
            try:
                return long_to_bytes(int(m[0]))
            except UnicodeDecodeError:
                pass
        

print(decrypt())