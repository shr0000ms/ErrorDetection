import socket
import random
import receiver_module
import error
import stats

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DC"
SERVER = "192.168.0.4"
CRC_KEY = "111010101"
ADDR = (SERVER, PORT)
ERROR_TYPE = 'burst'
FILENAME = 'data.txt'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)

def receive():
    frame_count = 0
    net_error_count = 0
    scheme_error_count = [0 for _ in range(4)]  # vrc_error, lrc_error, checksum_error, crc_error

    all_schemes = []
    check_not_crc = []
    vrc_not_crc = []

    not_vrc, not_lrc, not_cs, not_crc = [], [], [], []
    burst = 0

    while True:
        flag_error = False
        flag_scheme = [False for _ in range(4)]     # vrc_error, lrc_error, checksum_error, crc_error
        msg = client.recv(2048).decode(FORMAT)

        client.send("ACK".encode(FORMAT))

        if msg == DISCONNECT_MESSAGE:
            print('Disconnecting...')
            break

        frame_count += 1

        og_msg = msg
        if random.choice([True, False]):
            #print('Injecting error...')
            net_error_count += 1
            flag_error = True
            if ERROR_TYPE == 'burst':
                l = error.inject_burst(msg)
                msg = l[0]
                burst += l[1]
            else:
                msg = error.inject_bit(msg)

        if not receiver_module.checkvrc(msg[:32] + msg[32:32+1]):
            flag_scheme[0] = True
            scheme_error_count[0] += 1

        if not receiver_module.checklrc(msg[:32] + msg[33:33+8]):
            flag_scheme[1] = True
            scheme_error_count[1] += 1

        if not receiver_module.checkChecksum(msg[:32] + msg[41:41+8]):
            flag_scheme[2] = True
            scheme_error_count[2] += 1

        if not receiver_module.checkcrc(msg[:32] + msg[49:49+8], CRC_KEY):
            flag_scheme[3] = True
            scheme_error_count[3] += 1

        if all(flag_scheme):
            all_schemes.append((og_msg, msg))

        if flag_scheme[2] and not flag_scheme[3]:
            check_not_crc.append((og_msg, msg))

        if flag_scheme[0] and not flag_scheme[3]:
            vrc_not_crc.append((og_msg, msg))

        if flag_error and not flag_scheme[0]:
            not_vrc.append((og_msg, msg))
        if flag_error and not flag_scheme[1]:
            not_lrc.append((og_msg, msg))
        if flag_error and not flag_scheme[2]:
            not_cs.append((og_msg, msg))
        if flag_error and not flag_scheme[3]:
            not_crc.append((og_msg, msg))

    uncaught = (not_vrc, not_lrc, not_cs, not_crc)

    stats.show_stats(frame_count, net_error_count, scheme_error_count, all_schemes, check_not_crc, vrc_not_crc, uncaught, burst)


fname = FILENAME
client.send(fname.encode(FORMAT))
receive()
