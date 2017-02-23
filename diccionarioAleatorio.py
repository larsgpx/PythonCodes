import string
import random
import sys,os
 
palabra = str(raw_input("Ingrese una palabra: "))
tam = len(palabra)
caracter = ''
car = {}
contador=0
 
while True:
    if palabra != caracter:
        caracter=""
        contador+=1
        for i in range (0, tam):
            caracter += random.choice(string.letters)
 
        print caracter.lower() + ".resellervh.com.ve \n"
        os.system('echo '+caracter.lower()+' >> combinaciones.txt') #Guardar en archivo TXT
    else:
        print "Se encontro %s en %s veces" % (caracter,contador)
        sys.exit(1)
