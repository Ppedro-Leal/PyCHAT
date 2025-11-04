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
            # 1. Tenta a conexão inicial com o servidor
            self.socket.connect((self.HOST, self.PORT))
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor. Tente novamente.")
            return

        print("Conectado ao servidor com sucesso!")

        # LOOP PRINCIPAL DE REGISTRO DE APELIDO
        while self.running:
            # 2. Recebe a solicitação de apelido do servidor e envia o apelido        
            solicitacao = self.socket.recv(1024).decode()
            print(solicitacao, end="")

            self.nickname = input().strip()
            self.socket.send(self.nickname.encode())

            # 3. Recebe a resposta do servidor
            resposta = self.socket.recv(1024).decode()
            
            if resposta.startswith("ERR apelido_em_uso"):
                print("ERR APELIDO_EM_USO: apelido já em uso. Tente outro.")
                
                # O servidor fechou o socket. Precisamos de um novo socket para tentar novamente.
                self.socket.close()
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                try:
                    # Tenta reconectar a um novo socket
                    self.socket.connect((self.HOST, self.PORT))
                except ConnectionRefusedError:
                    print("Não foi possível reconectar. Servidor encerrado?")
                    self.running = False
                    return
                # Se a reconexão falhar, o loop 'while self.running' irá parar (ou tentar novamente).
                # Se a reconexão for bem-sucedida, o loop continua e pede um novo apelido.
                
            elif resposta.startswith("ERR"):
                print(f"Erro ao registrar: {resposta}")
                self.socket.close()
                self.running = False
                return
            else:
                # 4. Apelido aceito (Recebe a mensagem "Bem-vindo...")
                print(resposta)
                break # Sai do loop de registro, apelido aceito
        
        # O código só chega aqui se o apelido for aceito (com self.socket ativo)
        if not self.running:
            return

        Thread(target=self.receber_mensagem, daemon=True).start()
        self.enviar_mensagens()

    def receber_mensagem(self):
        while self.running:
            try:
                mensagem = self.socket.recv(1024).decode()
                if not mensagem:
                    print("Conexão encerrada pelo servidor.")
                    self.running = False
                    break

                # --- TRATAMENTO DE MENSAGENS DE ERRO DO SERVIDOR ---
                if mensagem.startswith("ERR"):
                    if "user_not_found" in mensagem:
                        print("ERR USER_NOT_FOUND: Usuário não encontrado.")
                    elif "apelido_em_uso" in mensagem:
                        print("Apelido já está em uso.")
                    else:
                        print(f"Erro do servidor: {mensagem}")
                    continue  # não imprime novamente a mesma mensagem

                # --- MENSAGENS NORMAIS ---
                print("\n" + mensagem)

            except ConnectionResetError:
                print("Conexão com o servidor perdida.")
                self.running = False
                break

            except Exception as e:
                print(f"Erro inesperado: {e}")
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
