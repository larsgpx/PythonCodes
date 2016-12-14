import os, time, commands, random, glob
from datetime import datetime, date, time, timedelta


tiempo = 61200
hostname = commands.getoutput('hostname')

print hostname
#actual = commands.getoutput('date +%H')
#actual = time.strftime('%Y-%m-%d %H:%M:%S')
fecha = '23'
late = datetime.strptime(fecha, '%H')

d = datetime.now()
a= d.strftime("%H")

actual = (23 - int(a))
#print actual



usuarios_general = commands.getoutput('cd /var/cpanel/users/;ls |cut -d "/" -f5 |sort|cut -d "." -f1 > /root/backup-users-py.txt')
usuarios_suspendidos = commands.getoutput('cd /var/cpanel/users/;grep -ilR SUSPENDED=1 * > /root/backup-users-Suspendidos-py.txt')
usuarios_activos = commands.getoutput('diff --line-format=%L backup-users-py.txt backup-users-Suspendidos-py.txt| cut -d "<" -f2 > /root/backup-users-Activos-py.txt')


archivo = open("backup-users-Activos-py.txt", "r")


#Clase COLA

class Cola(object):
    def __init__(self):
        self.items =[]

    def encolar(self, x):
        self.items.append(x)


    def esta_vacia(self):
        if len(self.items) == 0:
            return True
        else:
            return False

    def desencolar(self):
        if self.esta_vacia():
            return None
        else:
            return self.items.pop(0)

# cola de usuarios activos
def backups_active_users():
    colaUser = Cola()

    for linea in archivo.readlines():

        print ("usuario: " + linea)

        if colaUser.esta_vacia() == True:
            print "anadir a cola"
            colaUser.encolar(linea)

        elif actual >= 16 and actual < 23:
            print "Cola full"

            os.system('/scripts/pkgacct ' + colaUser.desencolar() + ' /backup/' + hostname)
            #print colaUser.desencolar()
        else:
            print "Aun no es hora para BACKUP"
            break

        #os.system('/scripts/pkgacct ' + linea + '/backup/' + hostname + '/') # ejecucion Sin cola
        continue
    return linea

    print len(colaUser.items)
    archivo.close()


#backups_active_users()  # print backup user


# Funcion para trabajos con delay usando SLEEP
def horario_preferencial():
    if actual == 06:
        print " comenzara el time.sleep hasta las 11pm"
        time.sleep(tiempo)
        #backups_active_users()
    elif actual >= 0 or 00 and actual < 17:
        print "Corre Script"
        backups_active_users()
    else:
        print "Algo pasa"

horario_preferencial()

def move_backup_home():
    if glob.glob("/home/cpmove*"):
        print "Hay cpmoves en Home, seran movidos a BACKUP"
        commands.getoutput('mv /home/cpmove-* /backup/' + hostname.rstrip('\n'))
    else:
        print "No hay CPMOVE en el directorio HOME"


move_backup_home()