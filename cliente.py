import socket
from threading import Thread

class Client:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def connect(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor tente novamente.")
            return

        print("Conectado ao servidor com sucesso!")

        # Recebe mensagem de solicitação de apelido
        print(self.socket.recv(1024).decode(), end="")
        self.nickname = input().strip()
        self.socket.send(self.nickname.encode())

        resposta = self.socket.recv(1024).decode()
        if resposta.startswith("ERR"):
            print("Apelido já em uso. Tente outro.")
            self.socket.close()
            return
        else:
            print(resposta)

        Thread(target=self.receber_mensagem, daemon=True).start()
        self.enviar_mensagens()

    def receber_mensagem(self):
        while self.running:
            try:
                mensagem = self.socket.recv(1024).decode()
                if not mensagem:
                    break
                print("\n" + mensagem)
            except ConnectionResetError:
                print("Conexão com o servidor perdida.")
                self.running = False
                break

    def enviar_mensagens(self):
        print("Você pode digitar mensagens, usar @apelido para DM, WHO para listar usuários ou QUIT para sair.\n")
        while self.running:
            try:
                msg = input()
                if not msg.strip():
                    continue

                if msg.upper() == "QUIT":
                    self.socket.send("QUIT".encode())
                    self.running = False
                    break

                self.socket.send(msg.encode())

            except KeyboardInterrupt:
                print("\nEncerrando conexão...")
                self.socket.send("QUIT".encode())
                self.running = False
                break

        self.socket.close()

if __name__ == "__main__":
    print("=== CLIENTE PyCHAT TCP ===")
    host = input("Digite o IP do servidor: ").strip()
    if not host:
        host = "127.0.0.1"
        print("Nenhum IP informado. Conectando ao localhost (127.0.0.1).")

    port_input = input("Digite a porta (padrão 7632): ").strip()
    port = int(port_input) if port_input else 7632

    client = Client(host, port)
    client.connect()
