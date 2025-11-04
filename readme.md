# Projeto Mini-Chat TCP com Python

Sistema de chat multiusuário cliente-servidor, desenvolvido em Python utilizando o protocolo TCP e concorrência via `threading`. O sistema atende a todos os requisitos propostos: registro de apelido único, mensagens de broadcast, mensagens diretas (DM) e comandos de sistema.

## Requisitos

* Linguagem: Python 3.x
* Transporte: TCP
* Concorrência: Múltiplas Threads

## Estrutura do Projeto

* `server.py`: Código do servidor de chat com console de administração.
* `cliente.py`: Código do cliente interativo em terminal.
* `Protocolo_Chat_TCP.docx`: Documento detalhando o protocolo de comunicação.

## Guia de Execução

O sistema foi configurado para ser executado tanto em uma máquina local (`127.0.0.1`) quanto em uma rede local (Wi-Fi/Ethernet).

### 1. Iniciar o Servidor (`server.py`)

O servidor escuta em todas as interfaces (`0.0.0.0`) na porta `7632` por padrão.

1.  Abra o terminal na pasta do projeto.
2.  Execute o servidor:

    ```bash
    python server.py
    ```

3.  O console do servidor exibirá o IP e a porta corretos para a conexão:
    * **Exemplo de saída:** `Endereço IP para conexão dos clientes: 192.168.X.X:7632` (Este IP deve ser usado pelos clientes).
    * **Console de Administração:** Após a inicialização, o servidor entrará em um console que permite listar usuários e desligar o sistema (Opções 1, 2 e 3).

### ⚠️ Nota Importante sobre Firewall (Rede Local)

Se você estiver conectando clientes de computadores diferentes na mesma rede e não conseguir a conexão (`Connection Refused`), é provável que o **Firewall** da máquina servidora esteja bloqueando a porta **7632**.

**Solução:** Crie uma **"Regra de Entrada"** no Firewall do Servidor para liberar a porta `7632` (TCP).

### 2. Conectar Clientes (`cliente.py`)

O cliente é interativo e solicitará o IP e a Porta.

1.  Abra um novo terminal para cada cliente (ou use máquinas diferentes).
2.  Execute o cliente:

    ```bash
    python cliente.py
    ```

3.  Insira as informações solicitadas:
    * **IP do servidor:** Digite o endereço IP exibido pelo console do servidor (ex: `192.168.1.10`). Se estiver testando apenas na máquina local, deixe vazio para usar o padrão (`127.0.0.1`).
    * **Porta:** Deixe vazio para usar a porta padrão (`7632`).

4.  Após a conexão, o cliente solicitará um **Apelido** (que deve ser único).

## Comandos de Sistema

Após o registro, o cliente pode usar os seguintes comandos:

| Comando | Função | Exemplo |
| :--- | :--- | :--- |
| **Broadcast (Padrão)** | Envia a mensagem a todos os usuários conectados. | `Pessoal, vou almoçar.` |
| **Mensagem Direta (DM)** | Envia a mensagem apenas ao destinatário. | `@Pedro me encontre na sala 201.` |
| **WHO** | Lista todos os apelidos dos usuários conectados. | `WHO` |
| **QUIT** | Encerra a conexão do cliente de forma limpa. | `QUIT` |

##  Casos de Teste 

Para testar, use o servidor e conecte pelo menos dois clientes, **`UserA`** e **`UserB`**.

| Caso de Teste | Ação (Remetente) | Resultado Esperado |
| :--- | :--- | :--- |
| **a. Broadcast** | `UserA` envia: `Teste de broadcast.` | `UserB` recebe: `FROM UserA [all]: Teste de broadcast.` |
| **b. DM para existente** | `UserA` envia: `@UserB Você recebeu o arquivo?` | **Apenas** `UserB` recebe: `FROM UserA [DM]: Você recebeu o arquivo?` |
| **c. DM para inexistente (erro)** | `UserA` envia: `@UserC Alguém viu o UserC?` | `UserA` recebe: `ERR user_not_found: Usuário inexistente.` |
| **d. Tentativa de apelido duplicado** | Novo cliente tenta se registrar como `UserA`. | O cliente recebe: `ERR APELIDO_EM_USO: Apelido já em uso. Tente outro.` e encerra a conexão. |