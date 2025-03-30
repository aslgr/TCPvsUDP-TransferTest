import socket
import os
import time

BUFFER_SIZE = 1024  # Tamanho do buffer
ARCHIVE_NAME = 'socm-video-17.mkv'

def receive_file_from_server(filename, addr, s):

    log_file = './Logs_UDP/logsUDP.txt'

    # Função para escrever no arquivo de log
    def write_to_log(message):
        with open(log_file, 'a') as log:
            log.write(message + '\n')

    # Envia uma mensagem inicial para o servidor para iniciar a transferência
    s.sendto(b'START', addr)

    # Inicia a contagem do tempo
    start_time = time.time()
        
    with open(filename, 'wb') as file:
        print("Iniciando recebimento do arquivo...")
        write_to_log("Iniciando recebimento do arquivo...")
        received_packets = 0  # Contador de pacotes recebidos
        total_bytes_received = 0  # Contador de bytes recebidos

        while True:
            # Recebe dados do servidor em pedaços de BUFFER_SIZE bytes
            data, _ = s.recvfrom(BUFFER_SIZE)  
                
            # Sai do loop se receber a mensagem de fim
            if data == b'END':
                break  
            
            # Escreve os dados recebidos no arquivo
            file.write(data)
            received_packets += 1
            total_bytes_received += len(data)
                
        print(f"Arquivo {filename} recebido com sucesso.")
        write_to_log(f"Arquivo {filename} recebido com sucesso.")
    
    # Calcula o tempo total de transferência
    end_time = time.time()
    total_time = end_time - start_time

    origem = f'../server_UDP/Arquivos_server_UDP/{ARCHIVE_NAME}'

    # Obtém o tamanho original do arquivo
    original_size = os.path.getsize(origem)
    # Calcula a quantidade de pacotes necessários
    num_packets = (original_size // BUFFER_SIZE) + 1

    # Chama a função para comparar os arquivos
    write_to_log("\n---------------------------------------------------")
    comparar_arquivos(origem, filename, write_to_log)
    write_to_log(f"Tempo da transferência:      {total_time:.5f} segundos")
    write_to_log(f"Tamanho original do arquivo: {original_size} bytes")
    write_to_log(f"Total de bytes recebidos:    {total_bytes_received} bytes")
    write_to_log(f"Pacotes necessários:         {num_packets}")
    write_to_log(f"Total de pacotes recebidos:  {received_packets}")
    write_to_log("---------------------------------------------------\n")

def comparar_arquivos(origem, destino, write_to_log):
    with open(origem, 'rb') as file1, open(destino, 'rb') as file2:
        if file1.read() == file2.read():
            message = "Todos os pacotes enviados foram recebidos corretamente."
            print(message)
            write_to_log(message)
        else:
            message = "Diferença detectada entre os arquivos de origem e destino."
            print(message)
            write_to_log(message)

if __name__ == '__main__':

    HOST = "127.0.0.1"  # Endereço padrão de loopback (localhost)
    PORT = 65433        # Porta para escutar (portas não privilegiadas são > 1023)

    # Cria socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

        # Caminho onde o arquivo será salvo
        filename = f'./Arquivos_client_UDP/{ARCHIVE_NAME}'
        receive_file_from_server(filename, (HOST, PORT), s)
