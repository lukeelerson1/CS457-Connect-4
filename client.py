import socket

def connect_to_server(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print("Connected to server at {}:{}".format(host, port))
        return client_socket
    except Exception as e:
        print("Failed to connect: {}".format(e))
        return None

def send_move(client_socket, column):
    try:
        message = "COLUMN {}".format(column)
        client_socket.send(message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print("Response from server: {}".format(response))
    except Exception as e:
        print("Error sending message: {}".format(e))

if __name__ == "__main__":
    client_socket = connect_to_server('localhost', 12345)
    if client_socket:
        while True:
            column = input("Enter a column to drop your piece (1-7) or 'exit' to quit: ")
            if column.lower() == 'exit':
                break
            send_move(client_socket, column)
    
    client_socket.close()
