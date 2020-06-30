import socket
import os
import logging

logging.basicConfig( #GPCG configuracion del loggin para pruebas
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

def recibeping():

    # Crea un socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    IP_ADDR = '167.71.243.238' #La IP donde desea levantarse el server
    #IP_ADDR_ALL = '' #En caso que se quiera escuchar en todas las interfaces de red
    IP_PORT = 9803 #Puerto al que deben conectarse los clientes

    BUFFER_SIZE = 64 * 1024 #Bloques de 16 KB


    # Bind the socket to the port
    serverAddress = (IP_ADDR, IP_PORT) 
    print('Iniciando servidor en {}, puerto {}'.format(*serverAddress))
    sock.bind(serverAddress)
    sock.listen(10) #El argumento indica la cantidad de conexiones en cola

    try:
        # Esperando conexion
        print('Esperando conexion remota')
        connection, clientAddress = sock.accept()
        print('Conexion establecida desde', clientAddress)
        print("Recibiendo audio...")
        archivo = open('stdRecibido.wav', 'wb') 
        buff = connection.recv(BUFFER_SIZE) #Los bloques se van agregando al archivo
        tamanio=buff.decode('utf-8')
        tamanio=int(tamanio)
        print('El tamanio del archivo en bytes es de: ', tamanio)
        ctamanio=0
        while(True):
            buff=connection.recv(BUFFER_SIZE)
            if (buff):
                archivo.write(buff)
                ctamanio = ctamanio + len(buff)
                #print('tamanio actual', ctamanio)00000000

            if (tamanio==ctamanio):
                print("Recepcion de audio finalizada")
                break
                    
    except KeyboardInterrupt:
            sock.close()

    finally:
            # Se baja el servidor para dejar libre el puerto para otras aplicaciones o instancias de la aplicacion
            sock.close()