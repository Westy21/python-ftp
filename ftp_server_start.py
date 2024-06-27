import socket
import threading
import os

class FTPServer:
    def __init__(self, directory, address, port):
        self.directory = directory
        self.address = address
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.address, self.port))
        self.server_socket.listen(5)
        print(f"Server started at {self.address}:{self.port}")

    def handle_client(self, client_socket):
        while True:
            try:
                command = client_socket.recv(1024).decode()
                if command.startswith("LIST"):
                    files = os.listdir(self.directory)
                    response = "\n".join(files)
                    client_socket.send(response.encode())
                elif command.startswith("DOWNLOAD"):
                    filename = command.split()[1]
                    filepath = os.path.join(self.directory, filename)
                    if os.path.exists(filepath):
                        with open(filepath, 'rb') as f:
                            while True:
                                bytes_read = f.read(1024)
                                if not bytes_read:
                                    break
                                client_socket.sendall(bytes_read)
                    client_socket.send(b"DONE")
                elif command.startswith("UPLOAD"):
                    filename = command.split()[1]
                    filepath = os.path.join(self.directory, filename)
                    with open(filepath, 'wb') as f:
                        while True:
                            bytes_read = client_socket.recv(1024)
                            if bytes_read.endswith(b"DONE"):
                                f.write(bytes_read[:-4])
                                break
                            f.write(bytes_read)
                else:
                    client_socket.send(b"Unknown command")
            except Exception as e:
                print(f"Error: {e}")
                break
        client_socket.close()

    def start(self):
        print("Waiting for connections...")
        while True:
            client_socket, _ = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: custom-ftp <directory> <address> <port>")
        sys.exit(1)
    directory, address, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
    server = FTPServer(directory, address, port)
    server.start()

