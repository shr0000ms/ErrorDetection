def checklrc(s):
    lrcbits = ""
    a, b, c, d = 0, 8, 16, 24
    for i in range(8):
        lrcbits = lrcbits + str(int(s[a+i]) ^ int(s[b+i]) ^ int(s[c+i]) ^ int(s[d+i]))
    return lrcbits == s[32:]


def checkvrc(s):
    sum = 0
    for c in s:
        if c != '0' and c != '1':
            return False
        if c == '1':
            sum += 1
    if sum % 2 == 0:
        return True
    return False


def checkChecksum(msg, k=8):
    c1 = msg[0:k]
    c2 = msg[k:2 * k]
    c3 = msg[2 * k:3 * k]
    c4 = msg[3 * k:4 * k]
    Checksum = msg[4 * k:]

    ReceiverSum = bin(int(c1, 2) + int(c2, 2) + int(c3, 2) + int(c4, 2) + int(Checksum, 2))[2:]

    if (len(ReceiverSum) > k):
        x = len(ReceiverSum) - k
        ReceiverSum = bin(int(ReceiverSum[0:x], 2) + int(ReceiverSum[x:], 2))[2:]

    ReceiverChecksum = ''
    for i in ReceiverSum:
        if (i == '1'):
            ReceiverChecksum += '0'
        else:
            ReceiverChecksum += '1'
    return int(ReceiverChecksum) == 0


def xor(a, b):
    result = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


def mod2div(dividend, divisor):
    pick = len(divisor)

    tmp = dividend[0: pick]

    while pick < len(dividend):

        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]

        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]

        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    checkword = tmp
    return checkword



def checkcrc(data, key):
    return int(mod2div(data, key), 2) == 0