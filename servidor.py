import socket

MAXBYTES = 65535


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 50000))

    while True:
        data, address = sock.recvfrom(MAXBYTES)

        if data == b'DISCOVERY':
            sock.sendto(b'READY', address)
        elif data[:5] == b'UPPER':
            sock.sendto(data[5:].upper(), address)
        elif data[:5] == b'LOWER': #Questao1A
            sock.sendto(data[5:].lower(), address)
        elif data[:3] == b'LEN':    #Questao1B
            sock.sendto(str(len(data[3:])).encode(), address)
        elif data[:5] == b'COUNT':  #Questao1C
            letra, address = sock.recvfrom(MAXBYTES)
            qtdL = data.decode().lower()[5:].count(letra.decode())
            sock.sendto(str(qtdL).encode(), address)
        elif data[:5] == b'WORDS':  #Questao1D
            contagem = len(data[5:].split())
            sock.sendto(str(contagem).encode(), address)
        elif data == b'BYE':
            sock.sendto('BYE', address)
            break
        else:
            sock.sendto(b'UNKNOWN', address)

    sock.close()
    return 0


if __name__ == '__main__':
    main()
