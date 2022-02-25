import requests
import socket
from bs4 import BeautifulSoup
import threading

HEADER = 64
PORT = 5050
# Run server first to get the IP
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def start():
    """
    need the words to run server
    Start the server and add a new thread for the new connection
    :return:
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def handle(conn, addr):
    print(f"new connection {addr}")
    connected = True

    while connected:
        # receive message
        message = conn.recv(1024).decode(FORMAT)
        if len(message):
            if message == DISCONNECT_MESSAGE:
                connected = False
            else:
                reply = parse_message(message)
                conn.send(reply.encode(FORMAT))

    # close the connection
    conn.close()


def parse_message(name):
    name.replace(" ", "_")
    wiki_adr = "https://en.wikipedia.org/wiki/" + name
    return get_page(wiki_adr)

def get_page(adr):
    page = requests.get(adr)
    print(page.status_code)
    print(type(page.status_code))
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        for para in soup.find_all("p"):
            print(para)
            print(len(para))
            if len(para) > 10:
                return para.get_text()
    return "Page could not be found"


start()