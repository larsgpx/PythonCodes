#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, commands, re, subprocess


#Primero que nada, hacer un backup del fstab antes de proceder con todo.


nfsDir01 = commands.getoutput('mount 10.0.100.2:/backup01 /backup/')
nfsInternoDir02 = commands.getoutput('mount 10.0.100.2:/nfs02 /Interbackup/')


NfsServers = ['re01.gconex.net', 'server-0008c.dnsprincipal.com','server-0008a.dnsprincipal.com','server-0008d.gconex.com']

output = commands.getoutput('yum list nfs-utils nfs-utils-lib | grep -x "Installed Packages"')
#output = subprocess.call(["yum list nfs-utils nfs-utils-lib | grep -x 'Installed Packages'"], stdout = subprocess.PIPE, stderr = subprocess.PIPE )
hostname = os.system('hostname')

class Troubleshooting:
    def __init__(self):
        print "Se ejecuto "

    def nfs_client_installed(self):

        word = "Installed Packages"
        if word in output:
            print "Paquete instalado"
        else:
            print "No instalado, se procedera a instalar"
            os.system('yes|yum install nfs-utils nfs-utils-lib')

    def add_ip_ranges(self):

        ips_tcp = commands.getoutput('iptables -A INPUT -p tcp  --match multiport --d ports 111,662,875,892,2049,32769,32803 -j ACCEPT')
        ips_udp = commands.getoutput('iptables -A INPUT -p udp  --match multiport --d ports 111,662,875,892,2049,32769,32803 -j ACCEPT')
        os.system('service iptables reload')

    def test_print(self,mensaje):
        print mensaje

tester = Troubleshooting()


#Se requieren los hostname de los servidores consolidados para proceder
def run_add_nfs():
    if hostname == "re01.gconex.net":
        print "se ejecutara Troubleshooting antes de añadir servidor al NFS"
        tester.nfs_client_installed()
        tester.add_ip_ranges()
        nfsDir01
    elif hostname == "server-0008c.dnsprincipal.com" or "server-0008d.gconex.com" or "server-0008a.dnsprincipal.com":
        print "se ejecutara Troubleshooting antes de añadir servidor al NFS"
        tester.nfs_client_installed()
        tester.add_ip_ranges()
        nfsInternoDir02
    else:
        print "El hostname no esta"