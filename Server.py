from socket import *
import threading
import datetime

SERVER_PORT = 63464
MAX_CLIENTS = 3
clients = {}

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", SERVER_PORT))
serverSocket.listen(MAX_CLIENTS)

print("Server is now listening for connections...")

clientCount = 1
clientLock = threading.Lock()

file_repository = ['file1.txt', 'file2.txt', 'file3.txt']

def main(connectionSocket, address, clientName):
    global clients
    Time = datetime.datetime.now()
    TimeConnected = Time.strftime("%x %X")

    with clientLock:
        clients[clientName] = {'Connected': TimeConnected, 'Disconnected': "Still Connected.."}

    print(f"Hello {clientName}")

    try:
        while True:
            user_input = connectionSocket.recv(1024).decode()
            if not user_input:
                break

            print(f"Received from {clientName}: {user_input}")

            if user_input.lower() == "exit":
                break  

            elif user_input.lower() == "status":
                with clientLock:
                    status = f"{clientName}: {clients[clientName]}"
                connectionSocket.send(status.encode())

            elif user_input.lower() == "list":
                file_list = "\n".join(file_repository)
                connectionSocket.send(file_list.encode())

            elif user_input in file_repository:
                try:
                    with open(user_input, 'rb') as file:
                        file_data = file.read()
                    connectionSocket.send(file_data)
                except FileNotFoundError:
                    connectionSocket.send(b"File not found.")

            else:
                connectionSocket.send(f"{user_input} ACK".encode())

    except Exception as e:
        print(f"Error with {clientName}: {e}")

    finally:
       
        Time = datetime.datetime.now()
        TimeDisconnected = Time.strftime("%x %X")

        with clientLock:
            if clientName in clients:
                clients[clientName]['Disconnected'] = TimeDisconnected
                print(f"{clientName} disconnected at {TimeDisconnected}")
                del clients[clientName]

        connectionSocket.close()

while True:
    connectionSocket, address = serverSocket.accept()

    with clientLock:
        if len(clients) < MAX_CLIENTS:
            clientName = f"Client{clientCount:02d}"
            clientCount += 1
            threading.Thread(target=main, args=(connectionSocket, address, clientName), daemon=True).start()
        else:
            print(f"Server is full.")
            connectionSocket.send(b"Server full. Try again later.")
            connectionSocket.close()
