import socket

SERVER_IP = '167.71.243.238'
SERVER_PORT = 9803
BUFFER_SIZE = 64 * 1024

#Se crea el socket
sock = socket.socket()
#Se crea la coneccion
server_address = (SERVER_IP, SERVER_PORT)
print('Conectando a {} en el puerto {}'.format(*server_address))
sock.connect(server_address)


try:
    buff = sock.recv(BUFFER_SIZE)
    archivo = open('stdRecibido2.wav', 'wb') #Aca se guarda el archivo entrante
    while buff:
        buff = sock.recv(BUFFER_SIZE) #Los bloques se van agregando al archivo
        archivo.write(buff)

    archivo.close() #Se cierra el archivo

    print("Recepcion de archivo finalizada")

finally:
    print('Conexion al servidor finalizada')
    sock.close() #Se cierra el socket