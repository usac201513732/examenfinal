#import paho.mqtt.client as mqtt
import logging
import threading
import time
import os 
import sys
import binascii
import multiprocessing
from selec2 import *
from glob import *

chatusuarios=[] #GPCG listas vacias para llenar con tuplas

logging.basicConfig( #AAMS  configuración inicial del logging
    level = logging.INFO,
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )


def estatus (): #AAMS funcion para hilo de estatus de recepción de datos
    while True :
        logging.debug("Esperando publicaciones...")
        time.sleep(2)

qos = 2
#logging.info("archivo.read()")
def lineaporlinea(archivodelectura): #GPCG ciclo for para leer el archivo de texto y generar las tuplas para la suscripcion
    try:
        with open(archivodelectura, 'r') as miarchivo:
            for line in miarchivo:
                logging.info("usuarios/03/"+str(line.replace('\n',''))) #GPCG esta linea se uso para comprobar el contenido de cada elemento
                chatusuarios.append(("usuarios/03/"+str(line.replace('\n','')), qos))#GPCG se uso line.replace para eliminar el caracter nulo al final del path generado
                chatusuarios.append(("audio/03/"+str(line.replace('\n','')), qos))
    except IOError:
        logging.debug("Error")
    
    return chatusuarios

def lineaporlinea2(archivodelectura2): #GPCG ciclo for para leer el archivo de texto y generar las tuplas para la suscripcion
    try:
        with open(archivodelectura2, 'r') as miarchivo2:
            for line in miarchivo2:
                logging.info("usuarios/03/"+str(line.replace('\n',''))) #GPCG esta linea se uso para comprobar el contenido de cada elemento
                chatusuarios.append(("salas/03/"+str(line.replace('\n','')), qos))#GPCG se uso line.replace para eliminar el caracter nulo al final del path generado
                chatusuarios.append(("audio/03/03"+str(line.replace('\n','')), qos))
    except IOError:
        logging.debug("Error")
    
    return chatusuarios

def alive(): #PJHB Comando ALIVE
    while True:
        tramaFTR = (b'\x04' + b"$"+ b"201503502" + b"$") #PJHB Concatena el comando más el usuario
        pinulito = tramaFTR 
        publishData("comandos/03/201503502", pinulito) #PJHB publica en el topic deseado
        time.sleep(ALIVE_PERIOD) #PJHB Tiempo de espera para enviar el ALIVE



lineaporlinea('usuario1.txt')
lineaporlinea2('salas_usuario1.txt')
logging.info(lineaporlinea2('salas_usuario1.txt'))
client.subscribe(chatusuarios)
#PJHB Suscripciones a comandos 
client.subscribe("comandos/03/201503502")
client.subscribe("comandos/03/201513732")
client.subscribe("comandos/03/201503408")
client.subscribe("comandos/03/201612696")

t1 = threading.Thread(name = 'Esperando',
                        target = estatus,
                        args = (),
                        daemon = True
                        )
t2 = threading.Thread(name = 'Contador de 2 segundo', #PJHB Hilo para el comando ALIVE
                        target = alive,
                        args = (),
                        daemon = True
                        )
                       
client.loop_start() #AAMS se inicia el hilo y se mantiene en el fondo esperando publicaciones de suscriptores
t1.start()   
t2.start()


try:
    while True:
        holis = seleccion(input("1) Enviar Texto\n2) Enviar Audio\nSeleccionar: "))
        holis.chat()
        time.sleep(2)  

except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")
    if t1.isAlive():
        t1._stop()
        t2._stop()

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")
    sys.exit()