import random


def inject_burst(s):
    pos = random.sample(range(len(s)), random.randint(1, len(s) - 1))
    # print('inverting bits at positions', *pos)
    pos.sort()
    injected = [int(c) for c in s]
    print(f'Injecting error with burst length = {pos[-1]} - {pos[0]} = {pos[-1] - pos[0]}')
    for i in pos:
        injected[i] = 1 - injected[i]
    injected = ''.join([str(ele) for ele in injected])
    return [injected, (pos[-1]-pos[0])]


def inject_bit(s):
    pos = random.randint(0, len(s)-1)
    print(f'Injecting error at bit position {pos}')
    injected = [int(c) for c in s]
    injected[pos] = 1 - injected[pos]
    injected = ''.join([str(ele) for ele in injected])
    return injected

