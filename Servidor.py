import paho.mqtt.client as mqtt
from brokerData import *
from gestion_Us import subs
from manejo_entradas import *
import logging
import threading
import time
import os 
import sys


#----------------------------configucacion de logging----------------------------------#
logging.basicConfig( #LGHM  configuración inicial del logging
    level = logging.INFO, #LGHM Aqui se indica el nivel de visualizacion de los loggin
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )
#--------------------------------------------------------------------------------------#

#-------------------------------configucacion de mqtt----------------------------------#
def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")

def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)
    
def on_message(client, userdata, msg):
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.info("El contenido del mensaje es: " + str(msg.payload))
        wenas = manejo_servidor(str(msg.topic),msg.payload)
        wenas.manejo()
        wenas.comando_in()
        


client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto

def publishData(topic, value, qos = 0, retain = False): #GPCG Función para publicar datos 
    client.publish(topic, value, qos, retain)
#--------------------------------------------------------------------------------------#

client.subscribe(subs) #LGHM se toma de los archivos las suscripciones necesarias generadas automaticamente



client.loop_start() #LGHM se inicia el hilo y se mantiene en el fondo esperando publicaciones de suscriptores

ack = b'\x03'
ack2 = b'\x04'
destino = b"03S01"
comando = ack + b"$" + destino+ b"$"
#comando = b'\x09'
comando2 =ack2 + b"$" + destino

try:
    while True:
        #publishData("comandos/03/201503502",comando2)
        #publishData("comandos/03/201503502",comando)
        #time.sleep(10)
        pass
       

except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")    