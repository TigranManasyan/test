import socket
import threading
import os 
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(msg):
    for client in clients:
        try: 
            client.send(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                raise Exception("Disconnected")
            broadcast(msg)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                nicknames.remove(nickname)
            break

def receive():
    print(f"[*] Սերվերն աշխատում է http://{HOST}:{PORT} հասցեով․․․")
    while True:
        client, address = server.accept()
        print(f"[+] Միացում {str(address)}-ից")
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print(f"[+] Մուտքանունը` {nickname}")
        broadcast(f"[Server] {nickname}-ը միացավ չատին".encode('utf-8'))
        client.send("[Server] դուք հաջողությամբ միացաք չատին".encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client, ))
        thread.start()

if __name__ == "__main__":
    receive()