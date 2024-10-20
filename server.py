import socket
import threading
import json

board = [[None for _ in range(7)] for _ in range(6)]
connected_clients = []
current_player = 0

def drop_piece(column, player):
    global board
    for row in reversed(range(6)):
        if board[row][column] is None:
            board[row][column] = player
            return row
    return -1

def handle_client(client_socket, address):
    global connected_clients, current_player

    if len(connected_clients) >= 2:
        response = {"type": "error", "message": "Server full. Two players already connected."}
        client_socket.send(json.dumps(response).encode('utf-8'))
        client_socket.close()
        return

    connected_clients.append(client_socket)
    player_id = len(connected_clients) - 1

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            data = json.loads(message)
            message_type = data.get("type")

            if message_type == "join":
                response = {"type": "join_ack", "status": "success", "player_id": player_id}
                client_socket.send(json.dumps(response).encode('utf-8'))

            elif message_type == "move":
                if player_id != current_player:
                    response = {"type": "error", "message": "Not your turn!"}
                    client_socket.send(json.dumps(response).encode('utf-8'))
                    continue

                column = data.get("column")
                row = drop_piece(column, player_id)

                if row == -1:
                    response = {"type": "error", "message": "Column is full"}
                    client_socket.send(json.dumps(response).encode('utf-8'))
                else:
                    response = {
                        "type": "move_ack",
                        "status": "accepted",
                        "column": column,
                        "row": row,
                        "player_id": player_id
                    }
                    broadcast_message(response)
                    current_player = 1 - current_player

            elif message_type == "chat":
                broadcast_message(data)

            elif message_type == "quit":
                break

    except Exception as e:
        pass

    connected_clients.remove(client_socket)
    client_socket.close()

def broadcast_message(message_data):
    global connected_clients
    for client in connected_clients:
        try:
            client.send(json.dumps(message_data).encode('utf-8'))
        except Exception as e:
            pass

def start_server(host='localhost', port=12346):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_handler.start()
    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
