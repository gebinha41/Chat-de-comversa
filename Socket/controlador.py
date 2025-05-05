import subprocess
import time

# Inicia o servidor
def iniciar_servidor():
    print("Iniciando o servidor...")
    servidor = subprocess.Popen(['python', 'servidor.py'])
    time.sleep(3)  # Aguardar o servidor ficar online
    return servidor

# Inicia os dois clientes automaticamente
def iniciar_clientes():
    print("Iniciando os clientes...")
    cliente1 = subprocess.Popen(['python', 'Cliente_1.py'])  # Certifique-se de ter um script 'Cliente_1.py'
    cliente2 = subprocess.Popen(['python', 'Cliente_2.py'])  # Certifique-se de ter um script 'Cliente_2.py'
    return cliente1, cliente2

if __name__ == "__main__":
    # Inicia o servidor
    servidor = iniciar_servidor()

    # Inicia os clientes após 3 segundos
    cliente_1, cliente_2 = iniciar_clientes()

    # Aguardar a execução dos processos
    servidor.wait()  # Aguarda até que o servidor termine a execução
    cliente_1.wait()  # Aguarda até que o cliente 1 termine a execução
    cliente_2.wait()  # Aguarda até que o cliente 2 termine a execução
