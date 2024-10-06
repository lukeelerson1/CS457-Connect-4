import socket
import threading

def handle_client(client_socket, address):
    print("New connection from {}".format(address))
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print("Received from {}: {}".format(address, message))
            
            if message.startswith("COLUMN"):
                column = message.split()[1]
                response = "MOVE ACCEPTED: PIECE DROPPED IN COLUMN {}".format(column)
                client_socket.send(response.encode('utf-8'))
            else:
                client_socket.send("INVALID MOVE FORMAT".encode('utf-8'))

        except Exception as e:
            print("Error: {}".format(e))
            break

    print("Connection closed: {}".format(address))
    client_socket.close()

def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on {}:{}".format(host, port))
    
    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
