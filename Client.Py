import socket

PORT = 12345

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', PORT))
    client_name = client_socket.recv(1024).decode()
    print(f"Connected to server as {client_name}.")

    while True:
        message = input(f"[{client_name}] Enter message: ")
        client_socket.send(message.encode())

        if message == "exit":
            break
        response = client_socket.recv(1024).decode()
        print(f"[Server] {response}")

        
    client_socket.close()
    print("Disconnected from server.")

if __name__ == '__main__':
    start_client() 