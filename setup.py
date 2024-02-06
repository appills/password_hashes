from random import randrange, randbytes
from argon2 import PasswordHasher

i = 0
passwords = [[]]*10
with open("top_200_passwords.txt", "r") as fh:
    while i < 10:
        line = fh.readline().strip().split(',')
        passwords[i] = line[0]
        i+=1


# fill 100 users
users = []
tails = 0
heads = 0
for i in range(0, 100):
    coin = randrange(0, 10)
    if coin / 5 > 0.51:
        # prefer random password
        password = randbytes(12).hex()
        tails+=1
    else:
        # randomly select one from the top 10
        password = passwords[randrange(0, 10)]
        heads+=1
    # random usernames
    users.append([randbytes(16).hex(), password])

print(f'drew {tails} random passwords and {heads} top 10 passwords')

# oh god math
hash_len = 32
memusage = 64 * 2**10 # 64 MiB
parallel = 1
timecost = 3
ph = PasswordHasher(timecost, memusage, parallel)
for user in users:
    password_hash = ph.hash(user[1])
    user[1] = password_hash

with open('hashes.txt', 'w') as fh:
    for user in users:
        fh.write(user[0] + ',' + user[1] + '\n')
