import socket
import threading
import json
import argparse
import logging
import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLUMNS = 7
board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Connect4Client:
    def __init__(self, host, port):
        self.client_socket = self.connect_to_server(host, port)
        self.window = tk.Tk()
        self.window.title("Connect 4 Client")
        self.create_gui()
        self.update_board()
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def connect_to_server(self, host, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((host, port))
            logging.info(f"Connected to server at {host}:{port}")
            return client_socket
        except Exception as e:
            logging.error(f"Failed to connect: {e}")
            messagebox.showerror("Error", f"Failed to connect to server: {e}")
            self.window.destroy()

    def send_move(self, column):
        try:
            message = f"COLUMN {column}"
            self.client_socket.send(message.encode('utf-8'))
            logging.info(f"Sent move to server: {message}")
        except Exception as e:
            logging.error(f"Error sending message: {e}")

    def send_chat_message(self):
        chat_message = self.chat_entry.get()
        if chat_message.strip():
            try:
                message = f"CHAT {chat_message}"
                self.client_socket.send(message.encode('utf-8'))
                logging.info(f"Sent chat message: {chat_message}")
                self.chat_entry.delete(0, tk.END)
            except Exception as e:
                logging.error(f"Error sending chat message: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                data = json.loads(message)
                message_type = data.get("type")

                if message_type == "move_ack":
                    logging.info(f"Move accepted. Piece dropped in column {data.get('column') + 1} by player {data.get('player_id')}")
                    global board
                    board = data.get("board")
                    self.update_board()
                elif message_type == "chat":
                    logging.info(f"Chat: {data.get('message')}")
                    self.chat_log.insert(tk.END, f"Chat: {data.get('message')}\n")
                elif message_type == "game_over":
                    logging.info(data.get("message"))
                    messagebox.showinfo("Game Over", data.get("message"))
            except Exception as e:
                logging.error(f"Error receiving message: {e}")
                break

    def create_gui(self):
        # Create board display
        self.board_frame = tk.Frame(self.window)
        self.board_frame.grid(row=0, column=0, columnspan=7, pady=10)
        
        self.cells = [[tk.Label(self.board_frame, text=" ", width=4, height=2, relief="solid", font=("Arial", 16), bg="white") for _ in range(COLUMNS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLUMNS):
                self.cells[r][c].grid(row=r, column=c, padx=2, pady=2)
        
        # Create column buttons
        self.buttons = [tk.Button(self.window, text=f"Drop {col+1}", command=lambda c=col: self.send_move(c+1)) for col in range(COLUMNS)]
        for col, button in enumerate(self.buttons):
            button.grid(row=1, column=col, padx=5, pady=5)

        # Chat entry and log
        self.chat_log = tk.Text(self.window, height=10, state='disabled')
        self.chat_log.grid(row=2, column=0, columnspan=7, pady=5)
        
        self.chat_entry = tk.Entry(self.window, width=50)
        self.chat_entry.grid(row=3, column=0, columnspan=6, padx=5, pady=5)

        self.send_chat_button = tk.Button(self.window, text="Send", command=self.send_chat_message)
        self.send_chat_button.grid(row=3, column=6, padx=5, pady=5)

    def update_board(self):
        for r in range(ROWS):
            for c in range(COLUMNS):
                if board[r][c] is None:
                    self.cells[r][c].config(text=" ", bg="white")
                elif board[r][c] == 0:
                    self.cells[r][c].config(text="X", bg="red")
                elif board[r][c] == 1:
                    self.cells[r][c].config(text="O", bg="yellow")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Connect 4 Client')
    parser.add_argument('-i', '--host', type=str, required=True, help='IP address of the server')
    parser.add_argument('-p', '--port', type=int, required=True, help='Port number of the server')

    args = parser.parse_args()

    client = Connect4Client(args.host, args.port)
    if client.client_socket:
        client.run()
