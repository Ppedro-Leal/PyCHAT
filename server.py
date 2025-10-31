import socket
from threading import Thread

class Server:
    Clientes = []

    # Crio o socket em tcp pelo ipv4. socket Listen é quantidade limite de pessoas!
    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST,PORT))
        self.socket.listen(10)
        print('Esperando conexão no servidor.....')

    # Ver quem se conectou no server e adiciona na lista de clientes
    def nova_conexao(self):
        while True:
            cliente_socket, endereco = self.socket.accept()
            print(str(endereco) + " Se conectou ao servidor.")

            cliente_socket.send("Digite seu apelido: ".encode())
            cliente_nome = cliente_socket.recv(1024).decode().strip()

            # Verifica se apelido já existe
            if any(c['cliente_nome'] == cliente_nome for c in Server.Clientes):
                cliente_socket.send("ERR apelido_em_uso".encode())
                cliente_socket.close()
                continue

            cliente = {'cliente_nome': cliente_nome, 'cliente_socket': cliente_socket}
            Server.Clientes.append(cliente)

            self.mensagem_all(cliente_nome, f"User {cliente_nome} entrou no chat!")

            cliente_socket.send("Bem-vindo ao chat! Use WHO, QUIT ou @user".encode())
            Thread(target=self.handle_novo_cliente, args=(cliente,)).start()

    def handle_novo_cliente(self, cliente):
        cliente_nome = cliente['cliente_nome']
        cliente_socket = cliente['cliente_socket']
        
        
        while True:
            try:
                cliente_mensagem = cliente_socket.recv(1024).decode()
            except ConnectionResetError:
                self.mensagem_all(cliente_nome, f"{cliente_nome} desconectou inesperadamente.")
                Server.Clientes.remove(cliente)
                cliente_socket.close()
                break

            if not cliente_mensagem:
                continue

            cliente_mensagem = cliente_mensagem.strip()

            # QUIT
            if cliente_mensagem.upper() == "QUIT":
                self.mensagem_all(cliente_nome, f"{cliente_nome} deixou o chat.")
                Server.Clientes.remove(cliente)
                cliente_socket.close()
                break

            # WHO
            elif cliente_mensagem.upper() == "WHO":
                nomes = [c['cliente_nome'] for c in Server.Clientes]
                resposta = "Usuários conectados: " + ", ".join(nomes)
                cliente_socket.send(resposta.encode())

            # DM
            elif cliente_mensagem.startswith("@"):
                partes = cliente_mensagem.split(" ", 1)
                alvo_nome = partes[0][1:]
                conteudo = partes[1] if len(partes) > 1 else ""
                alvo = next((c for c in Server.Clientes if c['cliente_nome'] == alvo_nome), None)

                if alvo:
                    msg = f"FROM {cliente_nome} [DM]: {conteudo}"
                    alvo['cliente_socket'].send(msg.encode())
                else:
                    cliente_socket.send("ERR user_not_found".encode())

            # Broadcast
            else:
                self.mensagem_all(cliente_nome, cliente_mensagem)
                
                
    # ve todos os clientes e envia mensagem all
    # Sender name é variavel para armazenar quem enviou a mensagem
    def mensagem_all(self, sender_name, mensagem):
        for cliente in self.Clientes:
             if cliente['cliente_nome'] != sender_name:
                texto = f"FROM {sender_name} [all]: {mensagem}"
                cliente['cliente_socket'].send(texto.encode())

if __name__ == '__main__':
     server = Server('127.0.0.1', 7632)
     server.nova_conexao()