import socket
import threading
import sender_module

PORT = 5050
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '192.168.0.4'
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DC"
CRC_KEY = "111010101"

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def readfile(fname):
    file = open(fname, "r")
    s = file.read()
    return s


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    fname = conn.recv(2048).decode(FORMAT)

    s = readfile(fname)

    for i in range(len(s)//32):
        frame = s[i*32:i*32+32]
        print(f'Sending frame {i+1} of {len(s)//32}')
        codeword = frame + sender_module.vrc(frame) + sender_module.lrc(frame) + sender_module.Checksum(frame) + sender_module.crc(frame, CRC_KEY)
        print(f"Codeword = {codeword}")
        conn.send(codeword.encode(FORMAT))
        ack = conn.recv(2048).decode(FORMAT)
        if ack != "ACK":
            print(f'[BROKEN CONNECTION] Disconnecting {addr}')
            conn.close()
            return

    conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
    print(f'[CONNECTION ENDED] {addr} has disconnected.')

    conn.close()


def start():
    server.settimeout(10)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        except socket.timeout:
            print('Server socket timed out.')
            return


print("[STARTING] server is starting...")
start()