from socket import *

serverName = "localhost"
serverPort = 63464

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

clientSocket.settimeout(2) 

try:
    server_response = clientSocket.recv(1024).decode()

    if server_response == "Server full. Try again later.":
        print(server_response)  
        clientSocket.close()
        exit() 

except timeout:
    pass  
while True:
    userInput = input("Input a lowercase sentence: ")
    clientSocket.send(userInput.encode())

    if userInput.lower() == "exit":
        break

    data = clientSocket.recv(1024).decode()
    print("From Server:", data)

clientSocket.close()
print("Disconnected from server.")
