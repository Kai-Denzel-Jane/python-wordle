import socket

def submit_high_score(username, score, host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    message = f"{username}:{score}"
    client_socket.sendall(message.encode())
    client_socket.close()


def info_input(tries_remaining):
    port = int(input("Enter the server port: "))
    host = str(input("Enter the server IP: "))
    username = str(input("Enter your name: "))
    score = tries_remaining

    if port == 0 and host == "None":
        import main
        main.welcome()
    else:
        submit_high_score(username, score, host, port)

    return username, score, host, port

