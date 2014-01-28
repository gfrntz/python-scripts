#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: chainwolf@gmail.com
# 
# Какая-то ручная проверялка#
#
import argparse
import base64
import os, sys
import pymongo
from pymongo import MongoClient

parser = argparse.ArgumentParser(description='\033[1mCheck time change directory for Nagios\033[0m')
parser.add_argument('--host', action="store", 
                    help='Имя хоста, к которому ищем данные')
parser.add_argument('--stream', action="store", 
                    help='Имя стрима.')

parser.add_argument('--total', action="store_true",
                    help='total strings')

args = parser.parse_args()



# Для доступа к Namespace словарю используем vars(). Результатом будет хэш.
variables = vars(args)
#print variables

if variables['host'] and variables['stream']:
  print "Only one option!"
  sys.exit(1)


def connect_to_mongo():
  client = pymongo.MongoClient('127.0.0.1',27017)
  client.the_database.authenticate('grayloguser','graylogpassword',source='graylog2')
  return client.graylog2


db = connect_to_mongo()


last_result = db.message_counts.find().sort('_id', -1)[0]
#print last_result['total']

decode_hash = {}

#print last_result['hosts']
for key,value in last_result['hosts'].items():
#	print "Host id is - %s. Messages count - %s" % (base64.b64decode(key),value)
	decode_hash.update({base64.b64decode(key):value}) 

#print decode_hash
#print "++++++++++++"

if variables['total']:
  print last_result['total']
  sys.exit(0)

if variables['host']:
	try:
	  print(decode_hash[variables['host']])
	except:
	  print 0

if variables['stream']:
  row_streams_hash = {}
  for key, value in last_result['streams'].items():
    row_streams_hash.update({key:value})

  streams_names = {}
  cursor = db.streams.find()
  for i, value in enumerate(cursor):
    streams_names.update({value['_id']: value['title']})

  streams_hash = {}
  for key,value in streams_names.items():
    key = str(key)
    try:
      streams_hash.update({value: row_streams_hash[key]})
    except:
      streams_hash.update({value: 0})
  print streams_hash[variables['stream']]
