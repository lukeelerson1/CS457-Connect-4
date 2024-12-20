import socket
import threading
import json
import argparse
import logging

ROWS = 6
COLUMNS = 7
board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_board(board):
    """
    Prints the current state of the game board.
    """
    for row in board:
        print('\n')
        print(" | ".join(['X' if cell == 0 else 'O' if cell == 1 else ' ' for cell in row]))
    print("-" * (COLUMNS * 4 - 1))

def connect_to_server(host='localhost', port=12345):
    """
    Establishes a connection to the server at the specified host and port.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        logging.info(f"Connected to server at {host}:{port}")
        return client_socket
    except Exception as e:
        logging.error(f"Failed to connect: {e}")
        return None

def send_move(client_socket, column):
    """
    Sends a move request to the server, specifying the column where the piece should be dropped.
    """
    try:
        message = f"COLUMN {column}"
        client_socket.send(message.encode('utf-8'))
        logging.info(f"Sent move to server: {message}")
        response = client_socket.recv(1024).decode('utf-8')
        logging.info(f"Response from server: {response}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")

def send_chat_message(client_socket, chat_message):
    """
    Sends a chat message to the server.
    """
    try:
        message = f"CHAT {chat_message}"
        client_socket.send(message.encode('utf-8'))
        logging.info(f"Sent chat message: {chat_message}")
    except Exception as e:
        logging.error(f"Error sending chat message: {e}")

def receive_messages(client_socket):
    """
    Listens for incoming messages from the server and processes them accordingly.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            data = json.loads(message)
            message_type = data.get("type")

            if message_type == "move_ack":
                logging.info(f"Move accepted. Piece dropped in column {data.get('column') + 1} by player {data.get('player_id')}")
                print_board(data.get("board"))
            elif message_type == "not_your_turn":
                logging.info("It's not your turn.")
            elif message_type == "chat":
                logging.info(f"Chat: {data.get('message')}")
            elif message_type == "game_over":
                logging.info(data.get("message"))
                logging.info("The game will now restart!")
            elif message_type == "player_left":
                logging.info(data.get("message"))
                print(data.get("message"))
        except Exception as e:
            logging.error(f"Error receiving message: {e}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Connect 4 Client')
    parser.add_argument('-i', '--host', type=str, required=True, help='IP address of the server')
    parser.add_argument('-p', '--port', type=int, required=True, help='Port number of the server')

    args = parser.parse_args()
    client_socket = connect_to_server(args.host, args.port)
    if client_socket:
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        while True:
            user_input = input("Enter 'move' to drop a piece, 'chat' to send a message, or 'exit' to quit: ").lower()

            if user_input == 'move':
                column = input("Enter a column (1-7): ")
                if column not in ['1', '2', '3', '4', '5', '6', '7']:
                    print("Invalid column. Please enter a number between 1 and 7.")
                    continue
                send_move(client_socket, column)

            elif user_input == 'chat':
                chat_message = input("Enter chat message: ")
                send_chat_message(client_socket, chat_message)

            elif user_input == 'exit':
                client_socket.send("quit".encode('utf-8'))
                logging.info("Client exiting...")
                break

        client_socket.close()
