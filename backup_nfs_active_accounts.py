import os, time, commands, random, glob
from datetime import datetime, date, time, timedelta


tiempo = 61200
hostname = commands.getoutput('hostname')

print hostname

backupdir = '/backup/' + hostname
#actual = commands.getoutput('date +%H')
#actual = time.strftime('%Y-%m-%d %H:%M:%S')
fecha = '23'
late = datetime.strptime(fecha, '%H')

d = datetime.now()
a= d.strftime("%H")

actual = (23 - int(a))
print "actual: " + str(actual)
print "a: " + str(a)


horas = [str(23),str(00),str(01),str(02),str(03),str(04),str(05),str(06)]

offhoras = [str(10),str(11)]

permitido = str(a) in horas

print permitido

#print str(permitido) + " <- permitido --- a -> " + str(a)

pkgprocess = commands.getoutput("ps aux | grep 'pkgacct' | grep -v grep| awk '{print $2}'|wc -l")
killprocess = commands.getoutput("for pid in $(ps -ef | awk 'pkgacct {print $2}'); do kill -9 $pid; done")

# Verificar si el directorio existe, en caso de que no exista, crearla con makedirs
backupdir = '/backup/' + hostname

if not os.path.exists(backupdir):
    os.makedirs(backupdir)
    print "creando directorio"

if not os.path.isfile("/root/backup-users-Activos-py-new.txt"):
    print "creando archivo.."
    os.mknod("/root/backup-users-Activos-py-new.txt")
else:
    print "ya existe archivo"


usuarios_general = commands.getoutput('cd /var/cpanel/users/;ls |cut -d "/" -f5 |sort|cut -d "." -f1 > /root/backup-users-py.txt')
usuarios_suspendidos = commands.getoutput('cd /var/cpanel/users/;grep -ilR SUSPENDED=1 * > /root/backup-users-Suspendidos-py.txt')
usuarios_activos = commands.getoutput('diff --line-format=%L backup-users-py.txt backup-users-Suspendidos-py.txt| cut -d "<" -f2 > /root/backup-users-Activos-py.txt')


archivo = open("backup-users-Activos-py.txt", "r")

#Funcion tipo Colas

lines = open('backup-users-Activos-py.txt').readlines()
file = open("backup-users-Activos-py-new.txt", "r")


vacio = os.stat("backup-users-Activos-py-new.txt").st_size == 0



# cola de usuarios activos
def backups_active_users():
    if permitido is True and vacio is False:
        for linea in file.readlines():
            #print ("usuario: " + linea)
            if int(pkgprocess) < 3:
                os.system('nice -n+20 /scripts/pkgacct --allow-override --incremental --compress ' + linea + '/backup/' + hostname + '/') # ejecucion Sin cola
                open('backup-users-Activos-py-new.txt', 'w').writelines(lines[1:-1])
                print "Corriendo.."
                continue
            else:
                print "No es la hora"
                break
    elif permitido is True and vacio is True:
        usuarios_activos
        print "Se recreara nuevamente la lista de usuarios activos.."
        print "Se correra el proceso de backups ahora.."
        os.system('nice -n+20 /scripts/pkgacct --allow-override --incremental --compress ' + linea + '/backup/' + hostname + '/') # ejecucion Sin cola        

        if int(pkgprocess) > 2:
            print "Hay varios procesos repetidos, se procedera a eliminarlos.."
            killprocess
    else:
        print "No es la hora para correr el Script"
        quit()




#-------------------
backups_active_users()  # print backup user


def backups_active_users_cola():
    colaUser = Cola()
    for linea in archivo.readlines():
        print ("usuario: " + linea)

        colaUser.esta_vacia()
        if colaUser.esta_vacia() == True:
            print "Cola vacia, anadir a cola"
            colaUser.encolar(linea)
            print colaUser
        elif actual >= 16 and actual < 23:
            print "Cola full"

            #os.system('/scripts/pkgacct ' + colaUser.desencolar() + backupdir)
            print colaUser
        else:
            print "Aun no es hora para BACKUP"
            break
        continue
    return linea

    print len(colaUser.items)
    archivo.close()



def move_backup_home():

    if glob.glob("/home/cpmove*"):
        print "Hay cpmoves en Home, seran movidos a BACKUP"
        commands.getoutput('yes|mv /home/cpmove-* /backup/' + hostname.rstrip('\n'))
    else:
        print "No hay CPMOVE en el directorio HOME"


move_backup_home()

def checking_congruencias():
	unexpectedFiles = commands.getoutput('ls /backup/'+hostname+'/*.0| wc -l')
	if int(unexpectedFiles) > 0:
		print "existe directorios .0"
		print "Seran eliminados"
		os.system('rm -vfr /backup/'+hostname+'/*.0') 
	else:
		print "No hay carpetas .0"


#checking_congruencias()
