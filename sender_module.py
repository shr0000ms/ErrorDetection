def vrc(s):
    xor = 0
    for c in s:
        xor = xor ^ int(c)
    return str(xor)


def lrc(s):
    lrcbits = ""
    a, b, c, d = 0, 8, 16, 24
    for i in range(8):
        lrcbits = lrcbits + str(int(s[a+i]) ^ int(s[b+i]) ^ int(s[c+i]) ^ int(s[d+i]))
    return lrcbits


def Checksum(msg, k=8):
    c1 = msg[0:k]
    c2 = msg[k:2 * k]
    c3 = msg[2 * k:3 * k]
    c4 = msg[3 * k:4 * k]

    Sum = bin(int(c1, 2) + int(c2, 2) + int(c3, 2) + int(c4, 2))[2:]

    if (len(Sum) > k):
        x = len(Sum) - k
        Sum = bin(int(Sum[0:x], 2) + int(Sum[x:], 2))[2:]
    if (len(Sum) < k):
        Sum = '0' * (k - len(Sum)) + Sum

    Checksum = ''
    for i in Sum:
        if (i == '1'):
            Checksum += '0'
        else:
            Checksum += '1'
    return Checksum


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



def crc(data, key):
    l_key = len(key)

    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)

    return remainder
