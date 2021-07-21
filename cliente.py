import socket

MAXBYTES = 65535

class TimeExceeded(OSError):
    pass


def find_server(sock):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    delay = 0.1
    aux = 0 #variavel auxiliar para a questao 2

    while True:
        sock.sendto(b"DISCOVERY", ('127.255.255.255', 50000))
        sock.settimeout(delay)
        try:
            data, address = sock.recvfrom(MAXBYTES)
        except socket.timeout:
            aux+=1
            if(aux==30):
                raise TimeExceeded

        else:
            print("Servidor encontrado em {}".format(address))
            break
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
    sock.settimeout(None)

    return address


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        address = find_server(sock)
    except TimeExceeded:
        print("Servidor não encontrado! Finalizando...")
        sock.close
        return
    
    sock.connect(address)

    while True:
        text = input("Texto: ")
        if text == 'bye':
            sock.send(b'BYE')
            data = sock.recv(MAXBYTES)
            break

        opcao = int(input('Opções:\n [1]UPPER \n [2]LOWER \n [3]LEN \n [4]COUNT \n [5]WORDS\n'))
        if opcao == 1:
            sock.send(b'UPPER' + text.encode())
        elif opcao == 2:
            sock.send(b'LOWER' + text.encode())
        elif opcao == 3:
            sock.send(b'LEN' + text.encode())
        elif opcao == 4:
            sock.send(b'COUNT' + text.encode())
            letra = input("Qual a letra deseja contar: ")
            sock.send(letra.encode())
        elif opcao == 5:
            sock.send(b'WORDS' + text.encode())
        data = sock.recv(MAXBYTES)
        print("Servidor responde: {}".format(data.decode()))

    sock.close()
    return 0


if __name__ == '__main__':
    main()
