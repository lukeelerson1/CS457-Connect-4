import socket
import threading
import json
import argparse
import logging

ROWS = 6
COLUMNS = 7
connected_clients = []
current_player = 0
board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]

logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def reset_board():
    global board
    board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
    logging.info("Board reset.")

def drop_piece(column, player_id):
    global board
    for row in range(ROWS-1, -1, -1):
        if board[row][column] is None:
            board[row][column] = player_id
            logging.info(f"Player {player_id + 1} dropped a piece in column {column + 1}.")
            return row
    return None

def check_winner(player_id):
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_id for i in range(4)):
                logging.info(f"Player {player_id + 1} wins by row.")
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player_id for i in range(4)):
                logging.info(f"Player {player_id + 1} wins by column.")
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_id for i in range(4)):
                logging.info(f"Player {player_id + 1} wins by diagonal.")
                return True
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == player_id for i in range(4)):
                logging.info(f"Player {player_id + 1} wins by anti-diagonal.")
                return True
    return False

def handle_client(client_socket, address):
    global connected_clients, current_player

    logging.info(f"New connection from {address}")

    if len(connected_clients) >= 2:
        client_socket.send("Server full. Two players already connected.".encode('utf-8'))
        client_socket.close()
        logging.warning(f"Connection attempt from {address} denied (server full).")
        return

    connected_clients.append(client_socket)
    player_id = len(connected_clients) - 1
    logging.info(f"Player {player_id + 1} connected.")

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            if message.startswith("COLUMN"):
                if player_id != current_player:
                    client_socket.send("Not your turn!".encode('utf-8'))
                    continue

                column = int(message.split()[1]) - 1
                if column < 0 or column >= COLUMNS:
                    client_socket.send("Invalid column!".encode('utf-8'))
                    continue

                row = drop_piece(column, player_id)
                if row is None:
                    client_socket.send("Column is full!".encode('utf-8'))
                    continue

                broadcast_message({
                    "type": "move_ack",
                    "column": column,
                    "row": row,
                    "player_id": player_id,
                    "board": board
                })

                if check_winner(player_id):
                    broadcast_message({
                        "type": "game_over",
                        "message": f"Player {player_id + 1} wins!"
                    })
                    reset_board()
                else:
                    current_player = 1 - current_player

            elif message.startswith("CHAT"):
                broadcast_message({
                    "type": "chat",
                    "message": message.split(' ', 1)[1]
                })

            elif message.lower() == 'quit':
                logging.info(f"Player {player_id + 1} disconnected.")
                break
    except Exception as e:
        logging.error(f"Error handling client {address}: {e}")

    logging.info(f"Connection closed: {address}")
    connected_clients.remove(client_socket)
    client_socket.close()

def broadcast_message(message_data):
    global connected_clients
    for client in connected_clients:
        try:
            client.send(json.dumps(message_data).encode('utf-8'))
        except Exception as e:
            logging.error(f"Broadcast error: {e}")

def start_server(host='localhost', port=12346):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logging.info(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Connect 4 Server')
    parser.add_argument('--host', type=str, default='localhost', help='IP address of the server')
    parser.add_argument('--port', type=int, default=12346, help='Port number of the server')

    args = parser.parse_args()
    start_server(args.host, args.port)
