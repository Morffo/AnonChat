from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
import socket
import select
from cryptography.fernet import Fernet



port = int(input("Введите желаемый порт: "))

def chat_client(screen):
    screen.clear_buffer(7, 0, 0)
    messages = []
    server_messages = []
    client_messages = []
    hostname = "37.140.192.226"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((hostname, port))
    print("You are connected!")
    input_line = ""

    def draw_chat():
        screen.clear_buffer(7, 0, 0)
        title = " Консольный Чат (Введите '~' для выхода) "
        screen.print_at(title.center(screen.width), 0, 0)
        screen.print_at('-' * screen.width, 0, 1, colour=7)
        for i, msg in enumerate(messages[-1000:], start=1):
            if msg in server_messages:
                screen.print_at(f"[host] {msg}", screen.width - len(msg) - 10, i + 1)
            elif msg in client_messages:
                screen.print_at(f"[guest] {msg}", 1, i + 1)
        screen.print_at('> ' + input_line, 0, len(messages) + 2, colour=6)

    
    while True:
        draw_chat()
        screen.refresh()

        # Проверка на наличие новых данных и событий
        readable, _, _ = select.select([client], [], [], 0.1)

        for sock in readable:
            data = sock.recv(1024)
            if data:
                message_encoded = data.decode()
                message = message_encoded
                messages.append(message)
                server_messages.append(message)

        event = screen.get_event()
        if isinstance(event, KeyboardEvent):
            if event.key_code in (10, 13) and input_line.strip():  # Enter
                client.send(input_line.encode())
                messages.append(input_line.strip())
                client_messages.append(input_line.strip())
                input_line = ""
            elif event.key_code == ord('~'):  # Tilde to quit
                break
            elif event.key_code in (-300, 127):  # Backspace
                input_line = input_line[:-1]
            else:
                input_line += chr(event.key_code)

    client.close()

Screen.wrapper(chat_client)
