import paho.mqtt.client as mqtt
from brokerData import *
import threading
import logging
import time
from clemisormetodo import * #Gerson estuvo aqui
from metodoreceptor import * #Geson estuvo aqui

logging.basicConfig( #GPCG configuracion del loggin para pruebas
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )
#-------------------------------configucacion de mqtt----------------------------------#

client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
#Se configura la funcion "Handler" que se activa al publicar algo
 #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto

def publishData1(topic, value, qos = 0, retain = False): #GPCG Función para publicar datos 
    client.publish(topic, value, qos, retain)
#--------------------------------------------------------------------------------------#

activos = ["03S01","03S02","03S03","201503502"]

class manejo_servidor (object):
    def __init__(self, topico, mensaje):
        self.topico = topico
        self.mensaje = mensaje

    def manejo (self):
        logging.info(self.topico)
        #logging.info(self.mensaje)


    def cliente_in (self):
        self.topico.split('/')[2]

    def comando_in (self): #GPCG funcion para determinar la accion recibida
        #logging.info(self.mensaje.split(b'$')[0])
        x = self.mensaje.split(b'$')[0] #GPCG tomando de la cadena de bits unicamente el commando
        y = str(self.mensaje)
        if x == b'\x04': #GPCG si se recibe un Alive
            logging.info("ALIVE")
            publishData1(self.topico,b'\x05$')
            logging.info("ACK")
            if self.topico.split('/')[2] in activos :
                pass
            else: 
                activos.append(self.topico.split('/')[2])                 
        elif x == b'\x03': #GPCG si se recibe un FTR
            logging.info("FTR")
            publishData1(self.topico,b'\x05$')
            logging.info("ACK")
            recibeping() #GPCG
            time.sleep(0.5)
            #logging.info(y.split('$')[1])
            #logging.info(activos)
            if (y.split('$')[1]) in activos:
                publishData1(self.topico,b'\x06$')
                logging.info("OK")
                f = open('servidor.wav', 'rb') #GPCG se crea un archivo f el cual se enviara, a partir del archivo prueba
                mamapinga(f)  
            else:
                publishData1(self.topico,b'\x07$')
                logging.info("NO")

 



#wenas = manejo_servidor("","")        
#wenas.manejo()


