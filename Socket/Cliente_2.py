import socket
import threading

HOST = 'localhost'
PORT = 12345

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

def receber():
    while True:
        try:
            msg = cliente.recv(1024).decode()
            if msg:
                print(msg)
        except:
            print("❌ Conexão encerrada.")
            cliente.close()
            break

def enviar():
    while True:
        try:
            msg = input()
            if msg:
                cliente.send(msg.encode())
        except:
            break

# Recebe e envia mensagens
thread_receber = threading.Thread(target=receber)
thread_receber.start()

thread_enviar = threading.Thread(target=enviar)
thread_enviar.start()
