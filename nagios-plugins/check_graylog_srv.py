#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: chainwolf@gmail.com
#
import argparse
import os, sys
import commands
parser = argparse.ArgumentParser(description='\033[1mGet host from graylog2 snmp script\033[0m')
parser.add_argument('-H', '--hostname', action="store", required=True,
                    help='Hostname'), 
parser.add_argument('--host', action="store", 
                    help='Получить хост')
parser.add_argument('--total', action="store_true", 
                    help='Получить все')
parser.add_argument('--stream', action="store", 
                    help='Получить stream'),
parser.add_argument('-c', '--critical', action="store", required=True, type=int,
                    help='Critical value'),
parser.add_argument('-w', '--warning', action="store", required=True, type=int,
                    help='Warning value')

args = parser.parse_args()

# Для доступа к Namespace словарю используем vars(). Результатом будет хэш.
variables = vars(args)
#print variables

# Количество сообщений от graylog2
msg_count = ""

if variables['total']:
  hash = {}
  cmd = "snmpwalk -v2c -Oq -Ov -c public %s graylog2_total_oid" % variables['hostname']
  cmd = commands.getoutput(cmd)
  cmd = cmd.replace("\"","").split("\n")
  for host in cmd:
    host = host.split(" - ")
    hash.update({host[0]: host[1]})

  msg_count = hash['Total']

elif variables['host']:
  hash = {}
  cmd = "snmpwalk -v2c -Oq -Ov -c public %s graylog2_host_oid" % variables['hostname']
  cmd = commands.getoutput(cmd)
  cmd = cmd.replace("\"","").split("\n")  
  for host in cmd:
    host = host.split(" - ")
    hash.update({host[0]: host[1]})

  try:
    msg_count = hash[variables['host'].split(".")[0]]
  except:
    msg_count = 0

elif variables['stream']:
  hash = {}
  cmd = "snmpwalk -v2c -Oq -Ov -c public %s graylog2_stream_oid" % variables['hostname']
  cmd = commands.getoutput(cmd)
  cmd = cmd.replace("\"","").split("\n")  
  for stream in cmd:
    stream = stream.split(" - ")
    hash.update({stream[0]: stream[1]})

  msg_count = hash[variables['stream']]

if int(msg_count) == "":
  print "UNKNOWN - Null msg count"
  sys.exit(3)

if int(msg_count) > variables['critical']:
  print "CRITICAL - Critical log msg value - %s" % msg_count
  sys.exit(2)
eilf int(msg_count) > variables['warning']:
  print "WARNING - Warning log msg value - %s" % msg_count
  sys.exit(1)
else:
  print "OK - log msg value - %s" % msg_count
  sys.exit(0)



