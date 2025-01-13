import socket
import threading


clients = []
server = socket.socket()            # создаем объект сокета сервера
hostname = "0.0.0.0"     # получаем имя хоста локальной машины
print(hostname)
port = int(input())                        # устанавливаем порт сервера
server.bind((hostname, port))       # привязываем сокет сервера к хосту и порту
server.listen(2)                    # начинаем прослушиваение входящих подключений

 
print("Server starts")

def broadcast(message, sender) -> None:
    for i in clients:
        if i != sender:
            i.send(message)

def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024)
        if not message:
            break
            
        print(f"Пришло сообщение: {message.decode()}")
        broadcast(message, client_socket)

 
while True:
    # Принимаем клиента
    client_socket, addr = server.accept()
    print(f"Клиент подключен: {addr}")
    clients.append(client_socket)

    # Запускаем поток для обработки клиента
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
