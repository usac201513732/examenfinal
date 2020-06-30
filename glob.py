
import binascii


ALIVE_PERIOD = 2 #Período entre envío de tramas ALIVE
ALIVE_CONTINUOUS = 0.1 #Período entre envío de tramas ALIVE si no hay respuesta

#COMMANDS
COMMAND_FTR = b'\x03' #Comando para enviar archivo de audio
COMMAND_ALIVE = b'\x04' #Comando para indicar la actividad de vida del cliente
COMMAND_ACK = b'\x05' #
COMMAND_OK = b'\x06' #
COMMAND_NO = b'\x07' #

#System filenames
USERS_FILENAME = 'usuarios'
ROOMS_FILENAME = 'salas'


#PJHB Variables extras
USER = []

heineken = ' '
lata = ' ' 
cont = 0