#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: chainwolf@gmail.com
#
import subprocess
import argparse
import snmp_passpersist as snmp

parser = argparse.ArgumentParser(description='\033[1mGet user memory usage\033[0m')
parser.add_argument('--user', action="store", 
                    help='Username')

args = parser.parse_args()

# Для доступа к Namespace словарю используем vars(). Результатом будет хэш.
variables = vars(args)
#print variables

def memory_usage():
    # cmd = commands.getoutput("pmap `pgrep -u %s` | grep total | awk \'{print $2}\' | awk \'{s+=$1}END{print s}\'") % (variables['user'])
    #cmd = subprocess.Popen("pmap `pgrep -u %s` | grep total | awk '{print $2}' | awk '{s+=$1}END{print s}'" % variables['user'], shell=True)
    output,error =subprocess.Popen("pmap `pgrep -u user` | grep total | awk '{print $2}' | awk '{s+=$1}END{print s}'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    print output.replace("\n","")
    #pp.add_int('1',cmd)

# def update():
#     memory_usage()

memory_usage()

# # Запускатор
# pp = snmp.PassPersist('oid')
# pp.start(update, 60)