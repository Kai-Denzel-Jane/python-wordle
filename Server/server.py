import threading
import socket
import pathlib

PORT = 8080  # Replace with the actual server port
HIGH_SCORES_FILE = pathlib.Path("./high_scores.txt")  # Replace with the actual file path

def handle_client(client_socket):
    data = client_socket.recv(1024).decode()
    username, score = data.split(":")
    score = int(score)  # Convert the score to an integer
    
    updated = False
    with open(HIGH_SCORES_FILE, "r") as file:
        lines = file.readlines()
    
    with open(HIGH_SCORES_FILE, "w") as file:
        for line in lines:
            existing_username, existing_score = line.strip().split(":")
            existing_score = int(existing_score)  # Convert the existing score to an integer
            if existing_username == username:
                if score > existing_score:  # Check if the new score is higher
                    file.write(f"{username}:{score}\n")
                    updated = True

                else:
                    file.write(line)  # Keep the existing high score
            else:
                file.write(line)
        
        if not updated:
            file.write(f"{username}:{score}\n")
    
    if updated:
        client_socket.sendall("EXISTS".encode())
    else:
        client_socket.sendall("ADDED".encode())
    
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", PORT))  # Replace "localhost" with the actual server IP address
    server_socket.listen(1)

    print("Server started. Listening for connections on port", PORT)

    while True:
        client_socket, address = server_socket.accept()
        print("New connection from:", address)

        # Start a new thread to handle the client
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
