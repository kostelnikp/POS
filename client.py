import socket
import threading
import datetime

HOST = "158.196.135.85"

reading = True

def read_thread():
    r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r.bind(("", 8010))
    while reading:
        received = r.recv(4096)
        msg = received[9:-1]
        date = datetime.datetime.fromtimestamp(int.from_bytes(received[4:8], "big"))
        length = received[8]
        crc = received[-1]
        crc_computed = 0
        for i in received[:-1]:
            crc_computed ^= i
        try:
            print(f"\033[F({length}) {'Y' if crc_computed == crc else 'N'} {date}: \"{msg.decode()}\"\n")
        except UnicodeDecodeError:
            print("\033[FAccepted invalid message!\n")
    r.close()

t1 = threading.Thread(target=read_thread)
t1.start()

while True:
    send = input("Write a message: ")
    if send == "":
        break
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, 8000))
    s.send(send.encode("ascii"))
    s.close()

print("Exiting...")
reading = False
t1.join()
