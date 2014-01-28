#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: chainwolf@gmail.com
#
import argparse
import os, sys
import commands
parser = argparse.ArgumentParser(description='\033[1mGet host from graylog2 snmp script\033[0m')
parser.add_argument('--host', action="store", 
                    help='Получить хост')
parser.add_argument('--total', action="store_true", 
                    help='Получить все')
parser.add_argument('--stream', action="store", 
                    help='Получить stream')

args = parser.parse_args()

# Для доступа к Namespace словарю используем vars(). Результатом будет хэш.
variables = vars(args)
#print variables


if variables['total']:
  hash = {}
  cmd = commands.getoutput('snmpwalk -v2c -Oq -Ov -c public graylog2_host graylog2_oid')
  cmd = cmd.replace("\"","").split("\n")
  for host in cmd:
    host = host.split(" - ")
    hash.update({host[0]: host[1]})

  print hash['Total']

elif variables['host']:
  hash = {}
  cmd = commands.getoutput('snmpwalk -v2c -Oq -Ov -c public graylog2_host graylog2_oid')
  cmd = cmd.replace("\"","").split("\n")  
  for host in cmd:
    host = host.split(" - ")
    hash.update({host[0]: host[1]})

  try:
    print hash[variables['host'].split(".")[0]]
  except:
    print 0

elif variables['stream']:
  hash = {}
  cmd = commands.getoutput('snmpwalk -v2c -Oq -Ov -c public graylog2_host graylog2_oid')
  cmd = cmd.replace("\"","").split("\n")  
  for stream in cmd:
    stream = stream.split(" - ")
    hash.update({stream[0]: stream[1]})

  print hash[variables['stream']]




