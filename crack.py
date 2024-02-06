from argon2 import PasswordHasher
from base64 import b64decode, standard_b64decode, urlsafe_b64decode

def parse_salt(h):
    delim = h.strip().removeprefix('$').split('$')

    return b64decode(delim[3] + "==", validate=False)

def get_hashes():
    hashes = []
    with open('hashes.txt', 'r') as fh:
        hashes = [line.strip().split(',', 1)[1] for line in fh]
    return hashes

i = 0
passwords = []
with open("top_200_passwords.txt", "r") as fh:
    while i < 10:
        line = fh.readline().strip().split(',')
        passwords.append(line[0])
        i+=1

hashes = get_hashes()
hash_len = 32
memusage = 64 * 2**10 # 64 MiB
parallel = 1
timecost = 3
ph = PasswordHasher(timecost, memusage, parallel)
for h in hashes:
    slt = parse_salt(h)
    for pword in passwords:
        if ph.hash(pword, salt=slt) == h:
            print(f'password: {pword} matched hash: {h}')