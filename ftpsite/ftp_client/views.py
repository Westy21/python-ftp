from django.shortcuts import render
from django.http import HttpResponse

import socket

FTP_SERVER_ADDRESS = '127.0.0.1'
FTP_SERVER_PORT = 2121

def list_files():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((FTP_SERVER_ADDRESS, FTP_SERVER_PORT))
        s.sendall(b'LIST')
        data = s.recv(1024).decode()
    return data.split('\n')

def download_file(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((FTP_SERVER_ADDRESS, FTP_SERVER_PORT))
        s.sendall(f'DOWNLOAD {filename}'.encode())
        with open(f'{filename}', 'wb') as f:
            while True:
                bytes_read = s.recv(1024)
                if bytes_read.endswith(b"DONE"):
                    f.write(bytes_read[:-4])
                    break
                f.write(bytes_read)

def index(request):
    files = list_files()
    return render(request, 'ftp_client/index.html', {'files': files})
    # return(HttpResponse("Hello world"))

def download(request, filename):
    download_file(filename)
    return HttpResponse(f"Downloaded {filename}")
