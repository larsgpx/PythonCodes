#!/usr/bin/python

import os,commands,time,datetime

# Detalles de la base de datos MySQL a la copia de seguridad que se hará. Asegúrese de que el usuario siguiente tenga suficientes privilegios para realizar copias de seguridad de las bases de datos.
# Para realizar varias copias de seguridad de bases de datos, cree cualquier archivo como /backup/dbnames.txt y baje los nombres de las bases de datos uno en cada línea y asignar a la variable DB_NAME.

DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = 'password'
#DB_NAME = '/backup/dbnames.txt' 
DB_NAME = 'db_name'
hostname = commands.getoutput('hostname')
BACKUP_PATH = '/backup/'

#Obtener la fecha y hora actuales para crear una carpeta de copia de seguridad independiente como por ejemplo -> "12012013-071334".
DATETIME = time.strftime('%m%d%Y-%H%M%S')

TODAYBACKUPPATH = BACKUP_PATH + DATETIME

# Verificar si el directorio existe, en caso de que no exista, crearla con makedirs
print "Creando directorio de backup"
if not os.path.exists(TODAYBACKUPPATH):
    os.makedirs(TODAYBACKUPPATH)

# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
print "Chequeando los nombres de las BDD."
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print "Base de datos encontrada"
    print "Inicio del backup de todos las BDD enumeradas en el archivo " + DB_NAME
else:
    print "Base de datos NO encontrada.."
    print "Comenzando backups... " + DB_NAME
    multi = 0

# Inicio del proceso real de backups de las BDD...
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")

   while p <= flength:
       db = dbfile.readline()   # Leyendo el nombre de la BDD del archivo..
       db = db[:-1]         # eliminando lineas extras
       dumpcmd = "mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"
       os.system(dumpcmd)
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = "mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"
   os.system(dumpcmd)

print "Backup completado"
print "Tus backups han sido creados en el directorio '" + TODAYBACKUPPATH