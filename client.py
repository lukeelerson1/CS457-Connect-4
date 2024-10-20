import socket
import threading
import json

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            data = json.loads(message)
            message_type = data.get("type")

            if message_type == "move_ack":
                print(f"Server: Move accepted. Piece dropped in column {data.get('column')}")
            
            elif message_type == "chat":
                print(f"{data.get('username')}: {data.get('message')}")
            
            elif message_type == "status":
                print(f"Server: {data.get('message')}")

        except Exception as e:
            break

def connect_to_server(username, host='localhost', port=12346):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        join_message = {"type": "join", "username": username}
        client_socket.send(json.dumps(join_message).encode('utf-8'))
        threading.Thread(target=receive_messages, args=(client_socket,)).start()
        return client_socket
    except Exception as e:
        return None

def send_message(client_socket, message_type, data):
    try:
        message = {"type": message_type, **data}
        client_socket.send(json.dumps(message).encode('utf-8'))
    except Exception as e:
        pass

if __name__ == "__main__":
    username = input("Enter your username: ")
    client_socket = connect_to_server(username)
    
    if client_socket:
        while True:
            user_input = input("Enter 'move' to drop a piece, 'chat' to send a message, or 'quit' to exit: ").lower()

            if user_input == 'move':
                column = int(input("Enter column (0-6): "))
                send_message(client_socket, "move", {"column": column})

            elif user_input == 'chat':
                chat_message = input("Enter chat message: ")
                send_message(client_socket, "chat", {"message": chat_message})

            elif user_input == 'quit':
                send_message(client_socket, "quit", {"username": username})
                break

    client_socket.close()
