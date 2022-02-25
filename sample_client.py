import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.56.1'  # Run server first
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send_request(game):
    msg = game.encode(FORMAT)
    client.send(msg)
    print(client.recv(2048).decode(FORMAT))

while True:
    game = input("Please enter name of video game or 'exit' to end: " )
    if game.lower() == "exit":
        break
    else:
        send_request(game)
