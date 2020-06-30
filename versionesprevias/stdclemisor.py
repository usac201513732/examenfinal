import socket
#import os
#import logging

SERVER_IP   = '167.71.243.238'
SERVER_PORT = 9803
BUFFER_SIZE = 64 * 1024

# Se crea socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se conecta al puerto donde el servidor se encuentra a la escucha
server_address = (SERVER_IP, SERVER_PORT)
print('Conectando a {} en el puerto {}'.format(*server_address))
sock.connect(server_address)

try:
    print('Conexion establecida a ', server_address)
    print('Enviando audio')
    while True:
        f = open('prueba.wav', 'rb') #GPCG se crea un archivo f el cual se enviara, a partir del archivo prueba
        bytes=f.read() #GPCG bytes es lo que se lee de f
        sock.sendall(str(len(bytes)).encode()) #GPCG se envia codificada la longitud del archivo
        sock.sendfile(f, 0) #GPCG se envia el archivo
        f.close()
        break
        
        print("\n\nArchivo audio enviado a: ", server_address)
    
finally:
    print('\n\nConexion finalizada con el servidor')
    sock.close() #GPCG se cierra el socket, este paso es muy importante para que el siguiente cliente pueda abrir ese socket y recibir el archivo