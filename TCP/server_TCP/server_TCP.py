import socket
import os

BUFFER_SIZE = 1024  # Tamanho do buffer
ARCHIVE_NAME = 'socm-video-17.mkv'

def send_file_to_client(filename, conn):

    # Obtém o tamanho do arquivo e calcula o número de pacotes
    file_size = os.path.getsize(filename)  
    num_packets = (file_size // BUFFER_SIZE) + 1  
            
    sent_packets = 0  # Contador de pacotes enviados
    
    # Lê o arquivo em pedaços de BUFFER_SIZE bytes
    with open(filename, 'rb') as file:
        while chunk := file.read(BUFFER_SIZE):
            # Envia cada pedaço do arquivo para o cliente
            conn.sendall(chunk)
            sent_packets += 1
        
    print(f"Arquivo {filename} enviado com sucesso.")
    print(f"Tamanho total transferido: {file_size} bytes")
    print(f"Total de pacotes enviados: {sent_packets}\n")

if __name__ == '__main__':

    HOST = "127.0.0.1"  # Endereço padrão de loopback (localhost)
    PORT = 12999        # Porta para escutar (portas não privilegiadas são > 1023)

    # Cria socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        # Associa o socket ao HOST e PORT especificados
        s.bind((HOST, PORT))
        
        # Habilita o servidor para aceitar conexões
        s.listen()

        # Espera e aceita conexão
        print("Servidor esperando por conexões...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexão estabelecida com {addr}")
                # Caminho do arquivo a ser enviado
                filename = f'./Arquivos_server_TCP/{ARCHIVE_NAME}'
                send_file_to_client(filename, conn)