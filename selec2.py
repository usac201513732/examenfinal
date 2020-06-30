import paho.mqtt.client as mqtt
from brokerData import *
from glob import *
from patitos import *
import threading
import time
import logging
import os
import sys
from clemisormetodo import *
from metodoreceptor import *

siome = ''
gallo = 'm'
gallo2 = ''
dorada = []
x = " "
#heineken = ' '

logging.basicConfig( #GPCG configuracion del loggin para pruebas
    level = logging.WARNING, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")

def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

def rep_audio(): #AAMS Funcion para hilo de reproducion de audio
    os.system('aplay Recibido.wav') #PJHB reproduce el audio luego de recibirlo

def grab_audio(tiempo, user):
    os.system('arecord -d '+str(tiempo)+' -f U8 -r 8000 prueba.wav')
    audio = open("prueba.wav", "rb") #PJHB Se abre el archivo de audio a enviar en bytes crudos
    #leer_audio = audio.read() #PJHB Lectura de la información del archivo de audio
    mamapinga(audio)#GPCG mamapingueando el audio
    audio.close() # PJHB Se cierra archivo de audio
    #enviar_audio = bytearray(leer_audio) #PJHB Se crea un arreglo de bytes en el cual se colocara cada byte del audio
    #topic = "comandos/03/201503502"
    #topic = "audio/03/"+user #AAMS construccion del topic 
    logging.debug(topic)
    #publishData(str(topic),enviar_audio) #AAMS publicando en el topic deseado
    logging.debug("audio enviado al usuario") #PJHB Se indica que ya se envió el audio

def aver(var): #PJHB Creacion de funcion para guardar el estado del FTR
    if var == "1":
        heineken = '1'
        gallo = heineken
        dorada.append(gallo)
        logging.info("de func." + gallo)
        return gallo

def alive2():
    while True:
        tramaFTR = (b'\x04' + b"$"+ b"201503502" + b"$") #PJHB Concatena el comando más el usuario
        pinulito = tramaFTR
        publishData("comandos/03/201503502", pinulito) #PJHB publica en el topic deseado
        time.sleep(ALIVE_PERIOD) #PJHB Temporizador para enviar cada 2 seg.

def last_alive(): #PJHB 
    while True:
        loggin.info("APURATE")
        tramaFTR = (b'\x04' + b"$"+ b"201503502" + b"$") #PJHB Concatena el comando más el usuario
        pinulito = tramaFTR
        publishData("comandos/03/201503502", pinulito) #PJHB publica en el topic deseado
        time.sleep(ALIVE_CONTINUOUS) #PJHB Temporizador para enviar cada 0.1 seg.


#def elcorreo(client, userdata, msg):
#    y = msg.payload
#    if y == b'\x06$':
#        logging.info("NIO")
#        print("NIO")
#        x = "1"
#        aver2("1")
#        seleccion.aver2(1)
#    return x


def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    papi = msg.payload
    chulo = str(msg.payload)
    siome = msg.payload
    if siome == b'\x06$':
            logging.info("ZI")
            print("ZI")
            aver("1")
            seleccion.aver2(1)

    if papi.split(b"$")[0]== b"\x02":  #GPCG si es audio proceder a reproducirlo
        logging.info("Ha llegado el audio:")
        #logging.info("Reproduciendo: ") 
        #data = msg.payload #PJHB Se asigna a la variable data la informacion entrante
        #file = open("Recibido.wav", "wb") #PJHB Crea archivo de audio
        #recibir_audio = file.write(data) #PJHB se sobre escribe el archivo de audio
        #file.close() #PJHB se cierra el archivo de audio
        recibeping()
        t3 = threading.Thread(name = 'Escuchando', #AAMS hilo para escuchar el audio y seguir programa principal
                        target = rep_audio,
                        args = (),
                        daemon = True
                        )
        t3.start()
    else: #AAMS si es texto tipo usuario o sala procede normalmente
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.info("El contenido del mensaje es: " + str(msg.payload))        
        wenas = str(msg.topic) 
        wenas2 = msg.payload
        #logging.info(wenas.split('/')[2]+': '+str(wenas2.decode('utf-8')))

    if chulo == b'\x05$':
        cont = 0
        t7 = threading.Thread(name = 'Alive', #PJHG hilo para verificacion de ALIVE
                        target = alive2,
                        args = (),
                        daemon = True
                        )
        t7.start()
    else: 
        cont = cont + 1     
        

#client.on_message = elcorreo
client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto


def publishData(topic, value, qos = 0, retain = False): #GPCG Función para publicar datos tipo chat
    client.publish(topic, value, qos, retain)

class seleccion(object): #GPCG clase para seleccion y envio de datos

    def __init__(self, sel):#GPCG Constructor
        self.sel = str(sel)

    def aver2(var): #PJHB Creacion de funcion para guardar el estado del FTR
        if var == 1:
            heineken = '1'
            gallo2 = heineken
            patitos.yawey(str(gallo2))
            logging.info("de func.2: " + gallo2) 
            print("variable gallo2: " + gallo2)
        return gallo2
    
    print(str(aver2))
 
    def chat(self):
        logging.debug(self.sel)
        #nuevo = input("1) Usuario\n2) Sala\nSeleccionar: ")
        if self.sel == str(1) :
            nuevo = input("1) Usuario\n2) Sala\nSeleccionar: ")    #AAMS seleccionar si usuario o sala
            if nuevo == str(1):
                user = input("Usuario destino: ") #AAMS escribir el carnet del usuario destino
                mensaje = input("Escriba mensaje: ")
                topic = "usuarios/03/"+user #AAMS construccion del topic 
                logging.debug(topic)
                publishData(str(topic),mensaje) #AAMS publicando en el topic deseado
                logging.debug("mensaje enviado al usuario")
            elif nuevo == str(2): #AAMS Si la eleccion fue una sala
                sala = input("Sala destino: ")
                mensaje = input("Escriba mensaje: ")
                topic = "salas/03/"+sala #AAMS construccion del topic 
                logging.info(topic)
                publishData(str(topic),mensaje) #AAMS publicando en el topic deseado
                logging.info("mensaje enviado a la sala")                
            else: logging.info("Accion no soportada")        
        elif self.sel == str(2) :
            nuevo = input("1) Usuario\n2) Sala\nSeleccionar: ") #AAMS seleccionar si usuario o sala
            if nuevo == str(1):
                user = input("Usuario destino: ") #AAMS escribir el carnet del usuario destino
                tiempo = str(input("Duracion de grabacion [s]: ")) #AAMS agregar duracion en segundos 
                #biuser = bytes(usr, "utf8") #PJHB Convierte la informacion del usuario a bytes
                tramaFTR = (b'\x03' + b"$"+ b"201503502" + b"$") #PJHB Concatena el comando más el usuario
                #logging.info(tramaFTR)
                pinulito = tramaFTR
                publishData("comandos/03/201503502", pinulito) #PJHB publica en el topic deseado
                dorada = str(patitos.yawey)
                print("pofavo: " + dorada)
                if dorada == "1":
                    tiempo = str(input("Duracion de grabacion [s]: ")) #AAMS agregar duracion en segundos 
                    logging.debug("audio enviado al usuario") #PJHB Se indica que ya se envió el audio
                    t = str(tiempo) 
                    t5 = threading.Thread(name = 'grabando', #AAMS hilo para grabar 
                            target = grab_audio,
                            args = (t,user),
                            daemon = True
                            )
                    t5.start()
                else:
                    print("Serivdor desconectado")

            elif nuevo == str(2): #AAMS Si la eleccion fue una sala
                sala = input("Sala destino: ")
                tiempo = str(input("Duracion de grabacion [s]: ")) #AAMS agregar duracion en segundos 
                biuser = bytes(user, "utf8") #PJHB Convierte la informacion del usuario a bytes
                tramaFTR = (COMMAND_FTR + biuser) #PJHB Concatena el comando más el usuario
                publishData(str(topic+user), tramaFTR) #PJHB publica en el topic deseado                
                t = str(tiempo)
                t6 = threading.Thread(name = 'grabando2', #AAMS hilo para grabar 
                        target = grab_audio,
                        args = (t,sala),
                        daemon = True
                        )
                t6.start()              
            else: logging.info("Accion no soportada") 
        else: logging.info("Accion no soportada")       



