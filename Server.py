import socket
import threading
from datetime import datetime

PORT = 12345        
MAX_CLIENTS = 3     

clients_cache = {}
file_repository = ['file1.txt', 'file2.txt', 'file3.txt']

def handle_client(client_socket, client_name):
    print(f"{client_name} connected.")
    
    clients_cache[client_name] = {
        'connection_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'disconnection_time': None  
    }

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"[{client_name}] {message}")

            if message == "status":
                status_message = "\n".join([f"{name}: {details}" for name, details in clients_cache.items()])
                client_socket.send(status_message.encode())
            elif message == "list":
                file_list = "\n".join(file_repository)
                client_socket.send(file_list.encode())
            elif message in file_repository:
                file_name = message
                with open(file_name, 'rb') as file:
                    file_data = file.read()
                client_socket.send(file_data)
            elif message == "exit":
                break
            else:
                client_socket.send(f"{message} ACK".encode())
        except Exception as e:
            print(f"Error: {e}")
            break

    clients_cache[client_name]['disconnection_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_socket.close()
    print(f"{client_name} disconnected.")

    # Remove the disconnected client from the cache
    del clients_cache[client_name]

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', PORT))
    server_socket.listen(5)
    print(f"Server started on {'localhost'}:{PORT}")

    client_count = 0

    while True:
        client_socket, client_address = server_socket.accept()
        if len(clients_cache) >= MAX_CLIENTS:
            client_socket.send(b"Server is full. Try again later.")
            client_socket.close()
            continue

        client_count += 1
        client_name = f"Client{client_count:02d}"
        client_socket.send(client_name.encode())
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
        client_thread.start()

if __name__ == "__main__":
    start_server()