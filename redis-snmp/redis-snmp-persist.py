#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: chainwolf@gmail.com
# 04 Jan 2014
#
# Version: 0.1.0
#

import commands
import argparse
import snmp_passpersist as snmp

parser = argparse.ArgumentParser(description='\033[1mRedis snmp-persist script\033[0m')
parser.add_argument('-H','--hostname', action="store", required=True,
                    help='Hostname машины с redis-сервером')
parser.add_argument('-p','--port', action="store", required=True,
                    help='Port redis-сервера'),
parser.add_argument('-o','--oid', action="store", 
                    help='Oid for redis-snmp-persist')

args = parser.parse_args()

# Для доступа к Namespace словарю используем vars(). Результатом будет хэш.
variables = vars(args)
# print variables # для отладки

base_oid = "Some_redis_oid.%s" % variables['oid']

def get_redis_info():
	cmd = "echo info | redis-cli -h %s -p %s" % (variables['hostname'],variables['port'])
	result = commands.getoutput(cmd)
	array = result.replace('\r','').split('\n')
	hash = {}
	key = ""
	for i in array:
		if "#" in i:
			key = i.replace('# ','')
			hash[key] = {}
		elif ":" in i:
			split_res = i.split(':')
			k,v = split_res[0],split_res[1]
			hash[key].update([(k,v)])
	return hash

def update():
	hash_result = get_redis_info()
	array_of_indexes = ['Server','Clients','Memory','Persistence','Stats','Replication','CPU','Keyspace']
	oid = 1
	for name in array_of_indexes:
		l_oid = 1
		i_hash = hash_result[name]
		pp.add_str(str(oid),name)
		for key,value in i_hash.iteritems():
			result = "%s %s" % (key,value)
			pp.add_str(str(oid)+'.'+str(l_oid),key)
			pp.add_str(str(oid)+'.'+str(l_oid)+'.'+str(1),value)
			l_oid += 1
		oid += 1

# Запускатор
pp = snmp.PassPersist(base_oid)
pp.start(update, 60)

