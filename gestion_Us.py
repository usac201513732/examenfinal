


archivo = open("usuarios.txt", "r")
archivo2 = open("salas.txt", "r")

lista_sub_s = []
lista_s = []
lista_ID = []
lista_name = []
subs = []


for i in archivo:
    lista_sub_s.append(i)   
    
for i in archivo2:
    lista_s.append(i.replace('\n',''))     
      

for i in lista_sub_s:
    lista_ID.append(i.split(',')[0])
    lista_name.append(i.split(',')[1])
    
for i in lista_ID:
    subs.append(("comandos/03/"+i, 0))

