#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: chainwolf@gmail.com
# 
import argparse
import base64
import os, sys
import pymongo
from pymongo import MongoClient
import snmp_passpersist as snmp

# Тут подразумевался конфиг. Но его нет. Он божественно документирован.
parser = argparse.ArgumentParser(description='\033[1mGet same graylog2 data\033[0m')
parser.add_argument('--config', action="store", 
                    help='Конфиг с данными для подключения')

args = parser.parse_args()

# Для доступа к Namespace словарю используем vars(). Результатом будет хэш.
variables = vars(args)
#print variables

# Подключаемся к бд
def connect_to_mongo():
  client = pymongo.MongoClient('127.0.0.1',27017)
  client.the_database.authenticate('grayloguser','graylogpassword',source='graylog2')
  db = client.graylog2
  return db 

# Возвращает сумму сообщений
def get_total(res):
  pp.add_str('1.1',"Total - " + str(res['total']))

# Возвращаем количество хостов и сообщений
def get_hosts(res):
  oid = 1
  # Получаем список хостов в декодированном виде
  hosts = decode_host_hash(res)
  # lenght = len(hosts)
  for key,value in hosts.items():
    some_string = "{0} - {1}".format(key, value)
    pp.add_str('2.'+str(oid), some_string)
    oid += 1

# Махинации со стримами.
def get_streams(h,s):
  # Получаем из ключа streams из message_count таблицы id стрима и количество строк
  row_streams_hash = {}
  for key, value in h['streams'].items():
    row_streams_hash.update({key:value})

  # Из таблицы streams вытаскиваем id и имя 
  streams_names = {}
  for i, value in enumerate(s):
    streams_names.update({value['_id']: value['title']})

  # Связываем имена и значения. Если у стрима 0 строк, то присваиваем ему 0
  streams_hash = {}
  for key,value in streams_names.items():
    key = str(key)
    try:
      streams_hash.update({value: row_streams_hash[key]})
    except:
      streams_hash.update({value: 0})
  
  # Добавляем это в snmp
  oid = 1
  for key, value in streams_hash.items():
    string = "{0} - {1}".format(key, value)
    pp.add_str('3.'+str(oid), string)
    oid +=1

# Создаем пустой хэш для сбора данных и в цикле наполняем его, одновременно декодируя из base64 названия хостов
# Например 'cmUx': 17 певращается в re: 17
def decode_host_hash(res):
  hash = {}
  for key,value in res['hosts'].items():
    hash.update({base64.b64decode(key):value})
  return hash

def update():
  # Получаем объект для работы с mongi
  result = connect_to_mongo()
  # Получаем самые последине сообщения
  hosts = result.message_counts.find().sort('_id', -1)[0]
  # Получаем стримы
  streams = result.streams.find()
  # Работаем с этим делом
  get_total(hosts)
  get_hosts(hosts)
  get_streams(hosts,streams)
  

# Запускатор
pp = snmp.PassPersist('graylog2 oid')
pp.start(update, 60)


