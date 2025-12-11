# client.py
import socket
import threading

SERVER = "SERVER_IP"   # change to server IP
PORT = 9999

def listen(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print("From server:", data.decode())

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER, PORT))
    threading.Thread(target=listen, args=(sock,), daemon=True).start()
    try:
        while True:
            msg = input()
            if not msg:
                break
            sock.sendall(msg.encode())
    except KeyboardInterrupt:
        pass
    sock.close()

if __name__ == "__main__":
    main()
