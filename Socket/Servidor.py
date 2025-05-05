import socket
import threading

HOST = 'localhost'
PORT = 12345

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

clientes = []
nomes = {}

# Lista de palavras proibidas
palavras_proibidas = ['boboca', 'idiota', 'burro', 'palavrão']

# Banco de dados fictício para login e senha
usuarios = {
    'cliente1': 'senha1',
    'cliente2': 'senha2'
}

# Função para filtrar palavrões nas mensagens
def filtrar_palavras(msg):
    for palavra in palavras_proibidas:
        msg = msg.replace(palavra, '***')
    return msg

# Função para enviar mensagens para todos os clientes conectados
def broadcast(mensagem, remetente=None):
    for cliente in clientes:
        if cliente != remetente:
            try:
                cliente.send(mensagem.encode())
            except:
                cliente.close()
                clientes.remove(cliente)

# Função de autenticação de cliente (login + senha)
def autenticar(cliente):
    cliente.send("Digite seu nome de usuário: ".encode())
    usuario = cliente.recv(1024).decode()

    cliente.send("Digite sua senha: ".encode())
    senha = cliente.recv(1024).decode()

    if usuario in usuarios and usuarios[usuario] == senha:
        cliente.send(f"Autenticação bem-sucedida. Bem-vindo, {usuario}!\n".encode())
        return usuario
    else:
        cliente.send("Nome de usuário ou senha inválidos. Conexão encerrada.\n".encode())
        cliente.close()
        return None

# Função para lidar com cada cliente conectado
def lidar_com_cliente(cliente):
    try:
        usuario = autenticar(cliente)
        if usuario is None:
            return

        nomes[cliente] = usuario
        clientes.append(cliente)

        print(f"{usuario} entrou no chat.")
        broadcast(f"🔔 {usuario} está online!", cliente)

        while True:
            try:
                msg = cliente.recv(1024).decode()
                if msg:
                    # Notifica ao cliente que ele mandou a mensagem
                    cliente.send(f"Você mandou: {msg}\n".encode())

                    # Filtra a mensagem antes de enviá-la para os outros clientes
                    msg_filtrada = filtrar_palavras(msg)
                    broadcast(f"{usuario}: {msg_filtrada}", cliente)
            except Exception as e:
                print(f"Erro ao receber mensagem de {usuario}: {e}")
                break

    except Exception as e:
        print(f"Erro com o cliente {usuario}: {e}")
        cliente.send("Problema na conexão.".encode())

    # Desconectar cliente
    print(f"{nomes[cliente]} saiu.")
    broadcast(f"❌ {nomes[cliente]} saiu do chat", cliente)
    clientes.remove(cliente)
    cliente.close()

# Inicia o servidor
print("🔌 Servidor está online...")

# Aceita conexões
while True:
    try:
        cliente, endereco = servidor.accept()
        print(f"Nova conexão de {endereco}")
        thread = threading.Thread(target=lidar_com_cliente, args=(cliente,))
        thread.start()
    except Exception as e:
        print(f"Erro ao aceitar conexão: {e}")
