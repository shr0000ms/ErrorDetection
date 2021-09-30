import random

string = ''.join([random.choice(['0', '1']) for _ in range(pow(2, 18))])

with open('data.txt', 'w') as f:
    f.write(string)